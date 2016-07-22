import json, asyncio
from head import Head
from file_io import FileIO
from publisher import Publisher

@asyncio.coroutine
def run():
	print("Starting")
	data = FileIO.get_dict_from_json('data/default_startup_protocol.json')
	# instantiate publisher object
	pubber = Publisher(None)
	# instantiate head object
	print("Instantiate head object")
	head = Head(data['head'],pubber)
	print("Get locations")
	locations = {'x': 20, 'y': 20, 'z': 20, 'a': 20, 'b':20}
	head.move(locations)
	print("Commanded move")

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.call_soon(run())
