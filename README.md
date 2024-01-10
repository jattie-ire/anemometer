# 3D Printed Anemometer

This is the git code archive for a 3D printed anemometer with a raspberry pi data logger, published here: https://www.printables.com/model/617911-modular-anemometer-with-roller-scate-bearing

The Raspberry Pi runs an interrupt driven piece of code that gets triggered every time the anemometer reed switch is triggered and then calculates the radial speed and converts that to windspeed in various formats. 

The raw data is then further processed and converted into a better time series based format fit for graphing and reporting purposes. See the data processing archive for more details on this.
