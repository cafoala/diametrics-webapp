import plotly.express as px
import pandas as pd

df = px.data.tips()
fig = px.scatter(df, x="total_bill", y="tip", facet_col="smoker", color="sex", trendline="ols")
fig.show()

results = px.get_trendline_results(fig)
print(results)

print(results.query("sex == 'Male' and smoker == 'Yes'").px_fit_results.iloc[0].summary().as_html())