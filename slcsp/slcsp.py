import csv


class SLCSP():
    
    def __init__(self):
        self.plans = csv_as_list('plans.csv')
        self.zips = csv_as_list('zips.csv')
        self.zip_x_rates = csv_as_list('slcsp.csv')
    
    
    def get_lowest_unique_rate(self, state, rate_area, plan_type='Silver'):
        matching_plan_rates = {}
        unique_rates = []
        for plan in self.plans:
            if plan[1] == state and plan[2] == plan_type and plan[4] == rate_area:
                rate = plan[3]
                if str(rate) in matching_plan_rates:
                    matching_plan_rates[str(rate)] += 1
                else:
                    matching_plan_rates[str(rate)] = 1
        
        for rate,count in matching_plan_rates.items():
            if count == 1:
                unique_rates.append(rate)
        
        return float(min(unique_rates))


    def create_zip_x_rates_csv(self, output_filename):
        header = self.zip_x_rates.pop(0)
        
        for zipcode in self.zip_x_rates:
            zip_rate_area = []
            for _zip in self.zips:
                if zipcode[0] == _zip[0]:
                        state = _zip[1]
                        zip_rate_area.append(_zip[4])
            
            # Determine rate for zip
            if len(set(zip_rate_area)) == 1:
                try:
                    zipcode[1] = self.get_lowest_unique_rate(state, zip_rate_area[0])
                except Exception as e:
                    # Rate not found for zip
                    pass
        
        with open(output_filename, "w") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows([header]+self.zip_x_rates)


def csv_as_list(filename):
    with open(filename) as f:
        return list(csv.reader(f))


if __name__ == '__main__':
    slcsp = SLCSP()
    slcsp.create_zip_x_rates_csv('zip_x_rates.csv')

