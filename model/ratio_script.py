import pandas as pd
import numpy as np
from ratio import RegressionModel

model = RegressionModel()
#print(model.predict())
print(model.predict(use_macro=False))
""" df = pd.DataFrame({"name": ['Alfred', 'Batman', 'Catwoman'],
                   "toy": [np.nan, 'Batmobile', 'Bullwhip'],
                   "born": [pd.NaT, pd.Timestamp("1940-04-25"),
                            pd.NaT]})
df.dropna()
print(df) """


# year_prior = row['year']-years
#             home_match = self.history_df.loc[self.history_df['home_id'] == row['home_id']]
#             row_prior = home_match.loc[home_match['year'] == year_prior]

#             # Break if not found
#             if len(home_match)<2 or len(row_prior) < 1:
#                 break

#             # Create new row with home data, prev_year, prev_value, prev_value
#             row_prior = row_prior.drop("home_id", axis=1)
#             row_prior = row_prior.drop("year", axis=1)
#             row_prior = row_prior.values.tolist()[0]
#             row_prior = [row['year'], row['value']] + row_prior

#             # Add row to DataFrame
#             row_series =  pd.Series(row_prior, index=pred_df.columns)
#             pred_df = pred_df.append(row_series, ignore_index=True)

