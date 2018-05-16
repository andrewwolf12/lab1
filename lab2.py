from spyre import server
import re
import glob
import pandas as pd
import json


class StockExample(server.App):
	title = "Lab2 with Spyre"

	inputs = [{ "type":'dropdown',
                "label": 'Index',
                "options" : [   {"label": "All", "value":"All"},
				{"label": "VCI", "value":"VCI"},
                                {"label": "TCI", "value":"TCI"},
                                {"label": "VHI", "value":"VHI"}],
                "key": 'index',
                "action_id": "update_data"
				},
				
			  { "type": 'dropdown',
				"label": 'Province',
				"options": [
				{"label": "Cherkasy", "value": "1"},
				{"label": "Chernihiv", "value": "2"},
				{"label": "Chernivtsi", "value": "3"},
				{"label": "Crimea", "value": "4"},
				{"label": "Dnipropetrovs", "value": "5"},
				{"label": "Donets", "value": "6"},
				{"label": "Ivano-Frankivs", "value": "7"},
				{"label": "Kharkiv", "value": "8"},
				{"label": "Kherson", "value": "9"},
				{"label": "Khmel", "value": "10"},
				{"label": "Kiev", "value": "11"},
				{"label": "Kiev City", "value": "12"},
				{"label": "Kirovohrad", "value": "13"},
				{"label": "Luhans", "value": "14"},
				{"label": "Lviv", "value": "15"},
				{"label": "Mykolayiv", "value": "16"},
				{"label": "Odessa", "value": "17"},
				{"label": "Poltava", "value": "18"},
				{"label": "Rivne", "value": "19"},
				{"label": "Sevastopol", "value": "20"},
				{"label": "Sumy", "value": "21"},
				{"label": "Ternopil", "value": "22"},
				{"label": "Transcarpathia", "value": "23"},
				{"label": "Vinnytsya", "value": "24"},
				{"label": "Volyn", "value": "25"},
				{"label": "Zaporizhzhya", "value": "26"},
				{"label": "Zhytomyr", "value": "27"}],
				"key": 'p_id',
				"action_id": "update_data"},
				
			  { "input_type":"text",
                "variable_name":"year",
                "label": "Year",
                "value":1981,
                "key": 'year',
                "action_id":"update_data"},

              { "type":'slider',
                "label": 'Week1',
                "min" : 1,
				"max" : 52,
				"value" : 1,
                "key": 'week1',
                "action_id": 'update_data'},

              { "type":'slider',
                "label": 'Week2',
                "min" : 1,
				"max" : 52,
				"value" : 52,
                "key": 'week2',
                "action_id": 'update_data'}]

	controls = [{
		"type": "hidden",
		"id": "update_data"
	}]

	tabs = [ "Table","Plot",]

	outputs = [
		{
			"type": "plot",
			"id": "plot",
			"control_id": "update_data",
			"tab": "Plot"
		}, {
			"type": "table",
			"id": "table_id",
			"control_id": "update_data",
			"tab": "Table",
			"on_page_load": True
		}
	]

	def getData(self,params):
		index = params['index']
		p_id = params['p_id']
		year = params['year']
		week1 = params['week1']
		week2 = params['week2']
		f = glob.glob('vhi_id_{}_*.csv'.format(p_id))[0]
		df1 = pd.DataFrame()
		dfile = pd.read_csv(f, index_col=False, skiprows=1,
				 sep=r'\s+,*|,\s*', 
				 names=['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI'], engine = 'python')
		dfile=dfile[:-1]
		df1 = df1.append(dfile)
		file = glob.glob('vhi2_id_{}_*.csv'.format(p_id))[0]
		df2 = pd.DataFrame()
		dfile = pd.read_csv(file, index_col=False, skiprows=1,
				 sep=r'\s+,*|,\s*', 
				 names=['year', 'week', '0', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60', '65', '70', '75', '80', '85', '90', '95','100'], engine = 'python')
		dfile=dfile[:-1]
		df2 = df2.append(dfile)
		df = pd.concat([df1.iloc[:,:], df2.iloc[:,2:]], axis=1)
		result = df.loc[(df['year']==str(year)) & (df['week']>=week1) & (df['week']<=week2)]
		if (index == "All"):
				result = result[['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', '0', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60', '65', '70', '75', '80', '85', '90', '95','100']]
		else:
				result = result[['week',index]]
		return result

	def getPlot(self,params):
		index = params['index']
		year = params['year']
		week1 = params['week1']
		week2 = params['week2']
		df = self.getData(params).set_index('week')
		df = df.astype(float)
		plt_obj = df.plot(color='r')
		plt_obj.set_ylabel(index)
		plt_obj.set_title("Table for {}".format(index))
		fig = plt_obj.get_figure()
		return fig

app = StockExample()
app.launch(port=9094)
