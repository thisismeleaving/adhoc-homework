"""
Author: Berty Pribilovics

"""
import csv


def csv_as_list(filename):
    with open(filename) as f:
        return list(csv.reader(f))


def get_rate(state, rate_area, plan_type='Silver'):
    plans = csv_as_list('plans.csv')

    for plan in plans:
        if plan[1] == state and plan[2] == plan_type and plan[4] == rate_area:
            return plan[3]


def create_zip_x_rates_csv(output_filename):
    zip_x_rates = csv_as_list('slcsp.csv')
    header = zip_x_rates.pop(0)
    zips = csv_as_list('zips.csv')

    for zipcode in zip_x_rates:
        zip_rate_area = []
        for _zip in zips:
            if zipcode[0] == _zip[0]:
                    state = _zip[1]
                    zip_rate_area.append(_zip[4])
        
        # Determine rate for zip
        if len(set(zip_rate_area)) == 1:
            try:
                zipcode[1] = float(get_rate(state, zip_rate_area[0]))
            except:
                # Rate not found for zip
                pass
    
    with open(output_filename, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows([header]+zip_x_rates)


if __name__ == '__main__':
    create_zip_x_rates_csv('zip_x_rates.csv')

