from coolboards.models import Item


class Command(BaseCommand):
    help = "Unmarks every item as new"

    def handle(self, *args, **options):
        Item.objects.update(new=False)
        self.stdout.write(self.style.SUCCESS("Successfully unmarked all items as new"))
