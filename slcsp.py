import csv

zip_to_rate_area = {}
silver_plans = []


def process_zips():
    with open('zips.csv') as zips:
        csv_reader = csv.DictReader(zips)
        next(csv_reader)
        for row in csv_reader:
            if row["zipcode"] in zip_to_rate_area.keys():
                zip_to_rate_area[row["zipcode"]].add((row["state"], row["rate_area"]))
            else:
                zip_to_rate_area[row["zipcode"]] = {(row["state"], row["rate_area"])}


def process_silver_plans():
    with open('plans.csv') as plans:
        csv_reader = csv.DictReader(plans)
        next(csv_reader)
        for row in csv_reader:
            if row["metal_level"] == "Silver":
                silver_plans.append({
                    "rate_area": (row["state"], row["rate_area"]),
                    "rate": row["rate"]
                })


def process_slcsp():
    with open('slcsp.csv', 'r') as slcsp:
        with open('slcsp-output.csv', 'w') as output:
            fieldnames = ["zipcode", "rate"]

            csv_reader = csv.DictReader(slcsp)
            csv_writer = csv.DictWriter(output, fieldnames=fieldnames)

            row = next(csv_reader)

            csv_writer.writeheader()
            for row in csv_reader:
                row["rate"] = get_rate(row["zipcode"])
                csv_writer.writerow(row)
    with open('slcsp-output.csv', 'r') as result:
        csv_reader = csv.reader(result)
        for row in csv_reader:
            print(",".join(row))


def get_rate(zipcode):
    rate_areas = zip_to_rate_area[zipcode]
    if len(rate_areas) != 1:
        return ''
    
    rate_area = rate_areas.pop()

    silver_plans_rates = [plan["rate"] for plan in silver_plans if plan["rate_area"] == rate_area]

    if len(silver_plans_rates) <= 1:
        return ''
    else:
        slcsp = sorted(silver_plans_rates)[1]
        return "{:.2f}".format(float(slcsp))


if __name__ == "__main__":
    process_zips()
    process_silver_plans()
    process_slcsp()
