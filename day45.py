from pyspark.sql import SparkSession
spark = SparkSession.builder \
    .appName("Day45_Spark_Transformations") \
    .getOrCreate()
print("\n Spark Session Created\n")
print("="*60)
print("RDD TRANSFORMATIONS")
print("="*60)
data = [10, 20, 30, 40, 50]
rdd = spark.sparkContext.parallelize(data)
mapped = rdd.map(lambda x: x * x)
print("\nMapped (Square):", mapped.collect())
filtered = mapped.filter(lambda x: x > 1000)
print("Filtered (>1000):", filtered.collect())
total = rdd.reduce(lambda x, y: x + y)
print("Reduced (Sum):", total)
print("\n" + "="*60)
print("DATAFRAME OPERATIONS")
print("="*60)
data = [
    ("Alice", 25, 50000),
    ("Bob", 30, 60000),
    ("Charlie", 35, 70000),
    ("David", 40, 80000)
]
columns = ["Name", "Age", "Salary"]
df = spark.createDataFrame(data, columns)
df.show()
high_salary = df.filter(df.Salary > 60000)
print("\nHigh Salary Employees:")
high_salary.show()
updated_df = df.withColumn("Bonus", df.Salary * 0.10)
print("\nSalary with Bonus:")
updated_df.show()
avg_salary = df.groupBy().avg("Salary")
print("\nAverage Salary:")
avg_salary.show()
spark.stop()