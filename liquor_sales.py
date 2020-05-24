import csv
from collections import namedtuple, defaultdict
from datetime import datetime

SALES_DATA = "./data/ia_liquor_sales.csv"
NUM_TOP_COUNTIES = 10
NUM_TOP_SALES = 5
MIN_SALES = 10

Sale = namedtuple("Sale", "date item price")


def get_sales_by_county(data=SALES_DATA):
    """Extracts all sales from csv and stores them in a dictionary
    where keys are counties, and values is a list of sales(named tuples)"""
    counties = defaultdict(list)
    with open(data, encoding="utf-8") as f:
        for line in csv.DictReader(f):
            try:
                county = (line["County"]).upper()
                date = line["Date"]
                item = line["Item Description"]
                price = float(line["Sale (Dollars)"])
            except ValueError:
                continue

            s = Sale(date=datetime.strptime(date, "%m/%d/%Y"), item=item, price=price)
            counties[county].append(s)

    return counties


def get_average_sale(counties):
    """Filter counties with < MIN_SALES and calculate averge sale"""
    """, _calc_total(sales)"""
    return {
        (county, _calc_mean(sales), _calc_total(sales)): sales
        for county, sales in counties.items()
        if len(sales) >= MIN_SALES
    }


def _calc_mean(sales):
    """Helper method to calculate mean of list of Sale namedtuples"""
    prices = [s.price for s in sales]
    mean = sum(prices) / max(1, len(prices))
    return round(mean, 2)


def _calc_total(sales):
    """Helper method to calculate total of list of Sale namedtuples"""
    prices = [s.price for s in sales]
    total = sum(prices)
    return round(total, 2)


def print_results(counties):
    """Print counties ordered by highest total sales. For each county
    print sales also ordered by highest sales price."""
    fmt_county_entry = "{counter:>02}. {county:<52} ${avg} ${total}"
    fmt_sales_entry = "{date}] {item:<50} ${price}"
    sep_line = "-" * 60

    for counter, (avg_sale, sales) in enumerate(
        sorted(counties.items(), key=lambda x: float(x[0][1]), reverse=True)[
            :NUM_TOP_COUNTIES
        ],
        1,
    ):
        county, avg, total = avg_sale

        print()
        print(fmt_county_entry.format(counter=counter, county=county, avg=avg, total=total))
        print(sep_line)

        for s in sorted(sales, key=lambda s: s.price, reverse=True)[:NUM_TOP_SALES]:
            print(fmt_sales_entry.format(date=datetime.strftime(s.date, '%Y-%m'), item=s.item[:50], price=s.price))


def main():
    counties = get_sales_by_county()
    counties = get_average_sale(counties)
    print_results(counties)


if __name__ == "__main__":
    main()
