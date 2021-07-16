import pyvisa as visa


VISA_ADDRESS2 = 'USB0::10893::257::MY54500309::0::INSTR'
VISA_ADDRESS1 = 'USB0::10893::513::MY57700960::0::INSTR'
file1 = 'ardX.txt'
file2 = 'ardY.txt'

try:
	resourceManager = visa.ResourceManager()
	session1 = resourceManager.open_resource(VISA_ADDRESS1)
	session2 = resourceManager.open_resource(VISA_ADDRESS2)

	"""if session1.resource_name.startswith('ASRL') or session1.resource_name.endswith('SOCKET'):
		session1.read_termination = '\n'

	if session2.resource_name.startswith('ASRL') or session2.resource_name.endswith('SOCKET'):
		session2.read_termination = '\n'"""

	while True:
		session1.write('DATA.LAST?')
		session1.write('DATA.LAST?')
		idn1 = float((session1.read()).rstrip('\n'))

		session2.write('*TRG')
		session2.write('READ?')
		idn2 = float((session2.read()).rstrip('\n'))
		print(f"Real: {idn1}, Imaginary: {idn2}")
		with open(file1, 'w') as filetowrite:
			filetowrite.write(str(idn1))
		with open(file2, 'w') as filetowrite:
			filetowrite.write(str(idn2))
		#print(type(idn))

	session1.close()
	session2.close()
	resourceManager.close()

except visa.Error as ex:
	print('An error occurred: %s' % ex)

print('Done.')
