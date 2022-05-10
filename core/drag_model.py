from core.projectile import Projectile


def linear_interpolation(x1, y1, x2, y2, x):
    diff_x = x2 - x1
    diff_y = y2 - y1
    desired_x_diff = x - x1
    x_ratio = desired_x_diff / diff_x
    y = y1 + (diff_y * x_ratio)
    return y


def model_factory(speed_data, drag_data):
    def predict(x):
        previous_speed = 0
        previous_drag = 0
        index = 0
        for i, speed in enumerate(speed_data):
            if x - speed > 0:
                previous_speed = speed
                previous_drag = drag_data[i]
                index = i
            elif x == speed:
                return drag_data[i]
            else:
                break
        if drag_data.__len__() > index + 1:
            next_drag = drag_data[index + 1]
            next_speed = speed_data[index + 1]
            drag = linear_interpolation(previous_speed, previous_drag, next_speed, next_drag, x)
        elif index > 0:
            second_last_drag = drag_data[index - 1]
            second_last_speed = speed_data[index - 1]
            drag = linear_interpolation(second_last_speed, second_last_drag, previous_speed, previous_drag, x)
        else:
            return drag_data[0]
        return drag
    return predict


class DragCalculator:
    def __init__(self):
        self.speed_of_sound = 340.29
        self.g7_model = self.load_drag_model("mcg7.txt")
        self.g1_model = self.load_drag_model("mcg1.txt")

    def load_drag_model(self, model_file_name):
        with open("core/drag_model/" + model_file_name) as file:
            drag_model_content = file.read()
        lines = drag_model_content.split("\n")
        speed_data = []
        drag_data = []
        for line in lines:
            if line.__len__() == 0:
                continue
            mach_number, drag_coefficient = line.split("\t")
            mach_number = float(mach_number)
            drag_coefficient = float(drag_coefficient)
            meter_per_sec = mach_number * self.speed_of_sound
            speed_data.append(meter_per_sec)
            drag_data.append(drag_coefficient)
        model = model_factory(speed_data, drag_data)
        return model

    def calculate_drag_coefficient(self, projectile: Projectile):
        if hasattr(projectile, "ballistic_coefficient_g7"):
            model_drag_coefficient = self.g7_model(projectile.speed)
        elif hasattr(projectile, "ballistic_coefficient_g1"):
            model_drag_coefficient = self.g1_model(projectile.speed)
        else:
            raise Exception("Ballistic coefficient undefined")
        projectile_drag_coefficient = (projectile.mass_in_grams * model_drag_coefficient) /\
                                      (pow(projectile.diameter_in_mm, 2) * model_drag_coefficient)
        return projectile_drag_coefficient
