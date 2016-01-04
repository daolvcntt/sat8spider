
def list_get(array, key, default = ''):
	if key in array :
		return array[key]
	else :
		return default