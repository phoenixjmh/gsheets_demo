import dataio as IO
class Employee:
   

    def __init__(self, name):
        self.m_Name = name
        self.m_Five_day_avg_output = 0
        self.m_Five_day_output_arr = [0, 0, 0, 0, 0]

    def get_average_weekly(self):
        return sum(self.m_Five_day_output_arr) / 5

    def get_today_output(self):
        return self.m_Five_day_output_arr[-1]

    def update_average(self):
        self.m_Five_day_avg_output=self.get_average_weekly()

    def update_output(self, output_today):
        self.m_Five_day_output_arr.pop(0)
        self.m_Five_day_output_arr.append(output_today)

    def print_output(self):
        output_f = f"""
            {self.m_Name} Produced {self.get_today_output()} cells of work today
            {self.m_Name}'s Average this week is {self.get_average_weekly()}
        """
        print(output_f)

    # def to_dict(self):
    #     dict={
    #         "Name":self.name,
    #         "Today output":self.get_today_output(),
    #         "AverageOutput":self.get_average_weekly()
    #     }
    #     return dict

    def dump_json(self, filename):
        IO.write_data(self.__dict__, filename)


def test_employee():
    deb = Employee("Debra")
    deb.update_output(10)
    deb.update_output(5)
    deb.update_output(5)
    deb.update_output(5)
    deb.update_output(9)
    deb.print_output()
    deb.dump_json('deb.json')


test_employee()
