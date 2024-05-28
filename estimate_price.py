import numpy as np


def estimate_price(cu_t0, cu_t1, mileage):
	return (cu_t1 * mileage) + cu_t0


def get_thetas():
	tmp_t0 = 0
	tmp_t1 = 0
	try:
		with open(".saved.tmp", 'r') as file:
			tmp_t0 = float(file.readline())
			tmp_t1 = float(file.readline())
		print(f"Values found for thetas.")
	except FileNotFoundError:
		print("No values for thetas found.")
	except ValueError:
		print("Problem encountered while looking for thetas values.")
	finally:
		print(f"Using t0: {tmp_t0} and t1: {tmp_t1}\n")
	return tmp_t0, tmp_t1


if __name__ == '__main__':
	t0, t1 = get_thetas()

	try:
		car_mileage = int(input("How much mileage on your car ?\n>"))
	except ValueError:
		print("The mileage must be a number")
		exit(1)
	except KeyboardInterrupt:
		print("Exiting")
		exit(1)
	print(f"The estimated price of your car is {estimate_price(t0, t1, car_mileage)}")
