from collections import defaultdict
import csv
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent / 'results'


class PepParsePipeline:

    def open_spider(self, spider):
        self.dict = defaultdict(int)

    def process_item(self, item, spider):
        self.dict[item['status']] += 1
        return item

    def close_spider(self, spider):
        self.dict['Total'] = sum(self.dict.values())
        date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        BASE_DIR.mkdir(exist_ok=True)
        filename = BASE_DIR / f'status_summary_{date}.csv'
        with open(filename, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerows([
                ('Статус', 'Количество'),
                *self.results.items(),
                ('Total', sum(self.results.values()))
            ])