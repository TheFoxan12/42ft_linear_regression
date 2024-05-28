import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from estimate_price import estimate_price
from sys import argv


def gradient_descent(cu_t0, cu_t1, cu_learning_rate, data):
	tmp_t0 = 0
	tmp_t1 = 0
	m = len(data)
	for j in range(m):
		mileage = data.iloc[j].km_normalized
		price = data.iloc[j].price_normalized

		error = estimate_price(cu_t0, cu_t1, mileage) - price
		tmp_t0 += error
		tmp_t1 += error * mileage
	cu_t0 -= (cu_learning_rate / m) * tmp_t0
	cu_t1 -= (cu_learning_rate / m) * tmp_t1
	return cu_t0, cu_t1


if __name__ == '__main__':
	print("Starting the linear regression.")

	try:
		cars = pd.read_csv("data.csv")
	except FileNotFoundError:
		print("The training data was not found.")
		exit(1)

	param = False
	try:
		iteration = int(argv[1])
		param = True
	except (ValueError, IndexError):
		print("You can pass the number of iterations as a parameter")
		iteration = 10000

	try:
		mode = True if argv[(param is True) + 1] == "compare" else False
	except IndexError:
		mode = False
		print("You can choose the compare mode by passing compare as a parameter")

	km_min = cars['km'].min()
	km_max = cars['km'].max()
	price_min = cars['price'].min()
	price_max = cars['price'].max()
	cars['km_normalized'] = (cars['km'] - km_min) / (km_max - km_min)
	cars['price_normalized'] = (cars['price'] - price_min) / (price_max - price_min)

	t0 = 0
	t1 = 0
	learning_rate = 0.01
	step = iteration / 10 if iteration / 10 <= 5000 else 5000
	for i in range(iteration):
		t0, t1 = gradient_descent(t0, t1, learning_rate, cars)
		if i % step == 0:
			print(f"{i}")

	t0 = t0 * (price_max - price_min) + price_min
	t1 = t1 * ((price_max - price_min) / (km_max - km_min))
	print(f"Found theta0 = {t0}, theta1 = {t1}.")
	print("Saving...")
	try:
		with open(".saved.tmp", 'w') as file:
			file.write(str(t0))
			file.write("\n")
			file.write(str(t1))
	except Exception:
		print("An error has occurred while trying to save the thetas.")
	else:
		print("Done.")

	plt.scatter(cars.km, cars.price)
	plt.scatter(range(km_min, km_max), [estimate_price(t0, t1, x) for x in range(km_min, km_max)], color="red")

	if mode:
		model = LinearRegression()
		x = np.array(cars.km).reshape(-1, 1)
		y = np.array(cars.price)
		model.fit(x, y)
		results = model.score(x, y)
		print(f"Found t0 : {model.intercept_}, t1 : {model.coef_} with reference")
		plt.scatter(range(km_min, km_max),
					[estimate_price(model.intercept_, model.coef_, x) for x in range(km_min, km_max)],
					color="blue")

	plt.show()
