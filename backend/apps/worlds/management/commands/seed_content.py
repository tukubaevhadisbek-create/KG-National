from django.core.management.base import BaseCommand
from apps.worlds.models import Location, Category
from apps.items.models import Item
from apps.quests.models import Quest, QuestOption


class Command(BaseCommand):
    help = "Заполняет базу данных начальным контентом"

    def handle(self, *args, **options):
        self.stdout.write("Начало заполнения контента...")

        # 1. Локация
        location, _ = Location.objects.get_or_create(
            slug="boz_ui",
            defaults={
                "name_ky": "Боз үй",
                "description_ky": "Кыргыздын традициялуу турак жайы",
                "order": 1,
            },
        )

        # 2. Категория
        category, _ = Category.objects.get_or_create(
            slug="music_instruments",
            defaults={
                "name_ky": "Музыкалык аспаптар",
                "order": 1,
            },
        )

        # 3. Предмет 1 (Комуз)
        komuz, _ = Item.objects.get_or_create(
            slug="komuz",
            defaults={
                "location": location,
                "category": category,
                "name_ky": "Комуз",
                "description_ky": "Кыргыздын улуттук кылдуу аспабы.",
                "cultural_fact_ky": "Комуз өрүк жыгачынан жасалат.",
                "difficulty": Item.Difficulty.EASY,
                "discover_reward": 10,
            },
        )

        # Предмет 2 (Чыны — для вариантов в квесте)
        chyny, _ = Item.objects.get_or_create(
            slug="chyny",
            defaults={
                "location": location,
                "category": category,
                "name_ky": "Чыны",
                "description_ky": "Чай ичүүчү идиш.",
                "difficulty": Item.Difficulty.EASY,
                "discover_reward": 5,
            },
        )

        # 4. Квест
        quest, _ = Quest.objects.get_or_create(
            location=location,
            prompt_ky="Комузду тап.",
            defaults={
                "quest_type": Quest.QuestType.FIND_ITEM,
                "correct_item": komuz,
                "reward_coins": 10,
            },
        )

        # Варианты ответов для квеста
        QuestOption.objects.get_or_create(
            quest=quest,
            item=komuz,
            defaults={"order": 1},
        )
        QuestOption.objects.get_or_create(
            quest=quest,
            item=chyny,
            defaults={"order": 2},
        )

        self.stdout.write(
            self.style.SUCCESS("Успешно! База данных заполнена контентом.")
        )