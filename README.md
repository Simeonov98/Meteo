# Meteo

Meteo is a Python-based project designed to collect and process meteorological data from various sources. The project includes multiple web scrapers targeting different weather websites to aggregate comprehensive weather information.

The main idea is to track the accuracy of meteorological forecasts with the shortening of the period between the date of the prognosis and the actual weather on the given day. 

## Features

- **Web Scraping**: Utilizes custom scripts to extract weather data from multiple sources.
- **Data Processing**: Processes and organizes the collected data for analysis or display.

## Tools

- **NextJs**: Typescrpit, NodeJs, Tailwind, TRPC, Postgres
- **Selenium**

## Project Structure

The repository is organized as follows:

- `dalivali/`: Contains scripts related to scraping data from the "Dalivali" weather website.
- `freemeteo/`: Contains scripts related to scraping data from the "Freemeteo" weather website.
- `sinoptik/`: Contains scripts related to scraping data from the "Sinoptik" weather website.
- `main.py`: The main script that orchestrates the data collection process.
- `db.py` and `db2.py`: Modules responsible for database interactions.
- `requierments.txt`: Lists the Python dependencies required for the project.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Simeonov98/Meteo.git
   cd Meteo
   ```

2. **Install dependencies**:

   Ensure you have Python installed, then install the required packages:

   ```bash
   pip install -r requierments.txt
   ```

3. **Set up environment variables**:

   Create a `.env` file in the root directory to store necessary environment variables. Refer to the `.env.example` file for the required variables.

4. **Database setup**:

   Configure your database settings in `db.py` or `db2.py` as needed.

## Usage

To start the data collection process, run:

```bash
python main.py
```

This command will execute the main script, which in turn calls the individual scrapers and processes the collected data.
*Currentry working with Sofia, Plovdiv, Vidin

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgements

- [Dalivali](https://www.dalivali.bg/) for providing weather data.
- [Freemeteo](https://freemeteo.com/) for providing weather data.
- [Sinoptik](https://sinoptik.bg/) for providing weather data.
