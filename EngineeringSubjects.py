from tkinter import messagebox

class Subjects:
    def subject_choose(_sem, _year, _dep):
        """choose subject according to sem and year"""
        sem_choice = _sem
        user_year = _year
        department = _dep
        """This function is to choose the subject for particular semester and year"""
        if user_year == 2 and department == 'EXTC':
            if sem_choice == 'IV':
                subjects = ('Engineering Mathematics - IV', 'Signal and Systems',
                            'Principles of Communication Engineering', 'Linear Integrated Circuits',
                            'Micro Controllers', 'Python Programming')
                return subjects
            elif sem_choice == 'III':
                subjects = ('Engineering Mathematics - III', 'Network Theory', 'Electronics Devices Circuit',
                            'Electronic and Communication Systems', 'Digital Systems', 'C++ Programming')
                return subjects
            else:
                messagebox.showerror("Error 102", '"Error 102"')

        elif user_year == 2 and department == 'MECH':
            if sem_choice == 'IV':
                subjects = ('Engineering Mathematics - III', 'Applied Thermodynamics', 'Fluid Mechanics',
                            'Manufacturing Processes', 'Kinematics of Machinery (Theory of Machines)- I')
                return subjects
            elif sem_choice == 'III':
                subjects = ('Solid Mechanics', 'Solid Modelling and Drafting', 'Engineering Thermodynamics',
                            'Engineering Materials and Metallurgy', 'Electrical and Electronics Engineering')
                return subjects
            else:
                messagebox.showerror("Error 103", "Error 103")

        # This will only work if the database has the data for students from the cs branch, Only for testing
        elif user_year == 2 and department == "CS":
            if sem_choice == "III":
                subjects = ('subject a', 'subject2', 'subjects c')
                return subjects
            elif sem_choice == "IV":
                subjects = ('subjects 1', 'subject 2', 'subject 3', 'subject 4')
                return subjects
            else:
                messagebox.showerror(
                    "Error 102", f"Error in subject\n{_sem}, {_dep}, {_year}")

        else:
            messagebox.showerror("Error 101", 'Error 101')
