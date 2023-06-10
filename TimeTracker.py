import re
import os
import signal
from datetime import datetime, timedelta
from tabulate import tabulate

class TimeTracker:
    def __init__(self):
        self.periods = []
        self.total_elapsed_time = timedelta()
        self.period_count = 1

    def calculate_elapsed_time(self, start_time, end_time):
        start_time = start_time.zfill(5)  # Asegura que el formato tenga 5 caracteres (HH.MM)
        end_time = end_time.zfill(5)  # Asegura que el formato tenga 5 caracteres (HH.MM)

        try:
            start = datetime.strptime(start_time, "%H.%M")
            end = datetime.strptime(end_time, "%H.%M")
            elapsed_time = end - start
            return elapsed_time
        except ValueError:
            print("\033[91mInvalid time format. Please enter time in HH.MM format.\033[0m")
            return timedelta()

    def get_time_input(self, prompt):
        while True:
            time_input = input(prompt)
            if re.match(r'^([01]?\d|2[0-3])(.([0-5]\d))?$', time_input):
                if len(time_input) == 1:  # Solo se ingresó un dígito para la hora
                    time_input = '0' + time_input
                elif len(time_input) == 2:  # No se especificaron minutos
                    time_input += '.00'
                return time_input
            elif time_input.strip().lower() == '':
                return None
            else:
                print("\033[91mInvalid time format. Please enter time in HH.MM format.\033[0m")

    def format_time_delta(self, time_delta):
        hours = time_delta.seconds // 3600
        minutes = (time_delta.seconds // 60) % 60
        return hours, minutes

    def display_elapsed_time(self, elapsed_time):
        elapsed_hours, elapsed_minutes = self.format_time_delta(elapsed_time)
        total_hours, total_minutes = self.format_time_delta(self.total_elapsed_time)

        print(f"\n\033[1mPeriod #{self.period_count}\033[0m")
        print(f"\033[1mElapsed time:\033[0m \033[94m{elapsed_hours} hours\033[0m and \033[94m{elapsed_minutes} minutes\033[0m")
        print(f"\033[1mTotal elapsed time:\033[0m \033[92m{total_hours} hours\033[0m and \033[92m{total_minutes} minutes\033[0m")
        terminal_width = os.get_terminal_size().columns
        line = '-' * terminal_width
        print(line)

    def display_results(self):
        headers = ["Period", "Start Time", "End Time", "Elapsed Time"]
        table_data = []

        for i, period in enumerate(self.periods, start=1):
            start_time = period['start_time'].replace('.', ':')
            end_time = period['end_time'].replace('.', ':')
            elapsed_time = self.format_time_delta(period['elapsed_time'])
            elapsed_time_str = f"\033[94m{elapsed_time[0]} hours {elapsed_time[1]} minutes\033[0m"
            table_data.append([i, start_time, end_time, elapsed_time_str])

        total_time = self.format_time_delta(self.total_elapsed_time)
        total_time_str = f"\033[92m{total_time[0]} hours {total_time[1]} minutes\033[0m"
        table_data.append(["Total", "", "", total_time_str])

        print("\n\n\033[1mTime Tracker Results\033[0m")
        print(tabulate(table_data, headers, tablefmt="fancy_grid"))

    def arreglar_formato_tiempo(self, tiempo):
        if len(tiempo) == 5:
            if tiempo[2] == '.':
                return tiempo
            else:
                return '0' + tiempo
        elif len(tiempo) == 4:
            return '0' + tiempo
        elif len(tiempo) == 2:
            return tiempo + '.00'
        elif len(tiempo) == 1:
            return '0' + tiempo + '.00'
        else:
            return None

    def run(self):
        while True:
            print(f"\n\033[1mPeriod #{self.period_count}\033[0m")
            start_time = self.get_time_input("Enter the start time (24-hour format, HH.MM) or leave blank to quit: ")

            if start_time is None:
                break

            start_time = self.arreglar_formato_tiempo(start_time)

            end_time = self.get_time_input("Enter the end time (24-hour format, HH.MM): ")
            end_time = self.arreglar_formato_tiempo(end_time)

            elapsed_time = self.calculate_elapsed_time(start_time, end_time)
            self.periods.append({'start_time': start_time, 'end_time': end_time, 'elapsed_time': elapsed_time})
            self.total_elapsed_time += elapsed_time

            self.display_elapsed_time(elapsed_time)
            self.period_count += 1

        self.display_results()


def handle_keyboard_interrupt(signal, frame):
    tracker.display_results()
    sys.exit(0)


if __name__ == "__main__":
    tracker = TimeTracker()
    signal.signal(signal.SIGINT, handle_keyboard_interrupt)
    try:
        tracker.run()
    except KeyboardInterrupt:
        handle_keyboard_interrupt(None, None)
