// Coolboards cart manager

// Cart is synced with cookies
const CartMgr = function (cartName) {
  let cart = {};
  try {
    cart = JSON.parse(Cookies.get(cartName));
  } catch (e) {
    console.log(cartName, e);
  }

  return {
    // Cart data
    cart: cart,

    // Cart subscription callbacks
    callbacks: [],

    // Call callbacks
    callCallbacks: function () {
      this.callbacks.forEach((callback) => callback(this.cart));
    },

    // Update cart
    updateCart: function () {
      // Iterate over items and delete items with quantity less than 1
      Object.keys(this.cart).forEach((item) => {
        if (this.cart[item] < 1) delete this.cart[item];
        if (typeof this.cart[item] === "string")
          this.cart[item] = parseInt(this.cart[item]);
      });

      // Update cookies and call callbacks
      Cookies.set(cartName, JSON.stringify(this.cart));
      this.callCallbacks();
    },

    // Set item quantity
    setItemQuantity: function (item, quantity) {
      this.cart[item] = parseInt(quantity);
      this.updateCart();
    },

    // Get item quantity
    getItemQuantity: function (item) {
      return this.cart[item] || 0;
    },

    // Add item to cart
    addItem: function (item) {
      if (this.cart[item]) this.cart[item]++;
      else this.cart[item] = 1;
      this.updateCart();
    },

    // Remove item from cart
    removeItem: function (item) {
      // Check if item is in cart
      if (!this.cart[item]) return;
      if (this.cart[item]) this.cart[item]--;
      if (this.cart[item] === 0) delete this.cart[item];
      this.updateCart();
    },

    // Subscribe to cart changes
    subscribe: function (callback) {
      this.callbacks.push(callback);
    },

    // Unsubscribe from cart changes
    unsubscribe: function (callback) {
      this.callbacks = this.callbacks.filter((cb) => cb !== callback);
    },

    // Clear cart
    clear: function () {
      this.cart = {};
      this.updateCart();
    },
  };
};

// Create cart manager
const cartMgr = CartMgr("cart");

// Subscribe elements to cart changes
document.querySelectorAll(".cart-quantity").forEach((cartQuantity) => {
  cartMgr.subscribe((cart) => {
    cartQuantity.innerText = Object.values(cart).reduce((a, b) => a + b, 0);
  });
});
document.querySelectorAll(".cart-item-quantity").forEach((cartQuantity) => {
  let isInput = cartQuantity.tagName === "INPUT";

  cartMgr.subscribe((cart) => {
    let key = isInput ? "value" : "innerText";
    cartQuantity[key] = cart[cartQuantity.dataset.item] || 0;
  });

  if (isInput)
    cartQuantity.addEventListener("change", (event) => {
      let value = parseInt(event.target.value);
      cartMgr.setItemQuantity(event.target.dataset.item, value || 0);
    });
});
document.querySelectorAll("button.add-to-cart").forEach((addToCart) => {
  let caption = addToCart.querySelector(".caption");
  cartMgr.subscribe((cart) => {
    if (!cart[addToCart.dataset.item]) {
      addToCart.classList.remove("item-exists");
      if (caption) caption.innerText = "В корзину";
    } else {
      addToCart.classList.add("item-exists");
      if (caption) caption.innerText = "Убрать";
    }
  });
  addToCart.addEventListener("click", (event) => {
    if (cartMgr.getItemQuantity(addToCart.dataset.item) === 0)
      cartMgr.addItem(addToCart.dataset.item);
    else cartMgr.setItemQuantity(addToCart.dataset.item, 0);
  });
});

// Cart page

function addTwoDecimalPlaces(number) {
  return parseFloat(number).toFixed(2).replace(".", ",");
}

document
  .querySelectorAll("table.cb-cart tr.item-cart-entry")
  .forEach((item) => {
    function checkRemoved(cart) {
      let quantity = cart[item.dataset.item] || 0;
      if (quantity === 0) {
        item.remove();
        cartMgr.unsubscribe(checkRemoved);
      }
    }
    cartMgr.subscribe(checkRemoved);
  });

document.querySelectorAll(".cb-cart-itemsum").forEach((itemSum) => {
  let item = itemSum.dataset.item;
  cartMgr.subscribe((cart) => {
    let quantity = cart[item] || 0;
    itemSum.innerText = addTwoDecimalPlaces(
      quantity * parseFloat(itemSum.dataset.priceforone)
    );
  });
});

document.querySelectorAll(".cb-cart-total").forEach((cartSum) => {
  cartMgr.subscribe((cart) => {
    console.log(ITEM_PRICES, cart);
    let sum = Object.entries(cart).reduce(
      (a, [id, quantity]) => a + quantity * ITEM_PRICES[id],
      0
    );
    cartSum.innerText = addTwoDecimalPlaces(sum);
  });
});

document.querySelectorAll(".cb-cart-empty").forEach((el) => {
  cartMgr.subscribe((cart) => {
    if (Object.keys(cart).length === 0) el.style.display = "block";
    else el.style.display = "none";
  });
});

document.querySelectorAll(".cb-cart").forEach((el) => {
  cartMgr.subscribe((cart) => {
    if (Object.keys(cart).length === 0) el.style.display = "none";
    else el.style.display = "block";
  });
});

// Force callbacks to update elements
cartMgr.callCallbacks();

// Create build manager
const buildMgr = CartMgr("build");

// Subscribe elements to build changes
document.querySelectorAll(".build-quantity").forEach((buildQuantity) => {
  buildMgr.subscribe((build) => {
    buildQuantity.innerText = Object.values(build).reduce((a, b) => a + b, 0);
  });
});
document.querySelectorAll("button.add-to-build").forEach((addToBuild) => {
  let caption = addToBuild.querySelector(".caption");
  buildMgr.subscribe((build) => {
    if (!build[addToBuild.dataset.item]) {
      addToBuild.classList.remove("item-exists");
      if (caption) caption.innerText = "В сборку";
    } else {
      addToBuild.classList.add("item-exists");
      if (caption) caption.innerText = "Убрать";
    }
  });
  addToBuild.addEventListener("click", (event) => {
    if (buildMgr.getItemQuantity(addToBuild.dataset.item) === 0)
      buildMgr.addItem(addToBuild.dataset.item);
    else buildMgr.setItemQuantity(addToBuild.dataset.item, 0);
  });
});

// Force callbacks to update elements
buildMgr.callCallbacks();
