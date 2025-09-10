import argparse
import asyncio
import random
import string
import sys
from datetime import datetime
from typing import List

from .database import prisma


def random_words(min_words: int = 2, max_words: int = 6) -> str:
    words = [
        "book", "task", "note", "item", "project", "idea", "plan", "goal",
        "meeting", "event", "reminder", "document", "file", "report", "review"
    ]
    selected = random.sample(words, k=random.randint(min_words, max_words))
    return " ".join(selected).title()


def random_suffix(length: int = 4) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def generate_title(index: int) -> str:
    base = random_words(1, 3)
    return f"{base} {random_suffix()}"


def generate_description() -> str:
    descriptions = [
        "Important task to complete",
        "Need to review this item",
        "Follow up required",
        "High priority item",
        "Regular maintenance task",
        "Quick action needed",
        "Long term project",
        "Weekly review item"
    ]
    return random.choice(descriptions)


async def seed_items(count: int, truncate: bool = False) -> List[int]:
    await prisma.connect()
    try:
        if truncate:
            await prisma.item.delete_many()

        created_ids = []
        async with prisma.tx() as tx:
            for i in range(count):
                title = generate_title(i)
                description = generate_description()
                created = await tx.item.create(
                    data={"title": title, "description": description}
                )
                created_ids.append(created.id)
        return created_ids
    finally:
        await prisma.disconnect()


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed database with sample items")
    parser.add_argument("--count", type=int, default=20, help="Number of items to create")
    parser.add_argument("--truncate", action="store_true", help="Clear existing items first")
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    start = datetime.utcnow()
    created_ids = asyncio.run(seed_items(count=args.count, truncate=args.truncate))
    duration = (datetime.utcnow() - start).total_seconds()
    print(f"Created {len(created_ids)} items in {duration:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
