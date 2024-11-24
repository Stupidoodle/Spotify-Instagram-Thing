# Spotify-Instagram-Thing

This project integrates Spotify and Instagram functionalities. It allows users to interact with both platforms through a unified interface.

## Project Structure

```
.gitattributes
.gitignore
src/
tests/
main.py
```

### Key Directories and Files

- **src/**: Contains the source code for the project.
  - **api/**: Contains API integrations for Spotify and Instagram.
    - 

spotify.py

: Spotify API integration.
    - 

instagram.py

: Instagram API integration.
- **tests/**: Contains unit tests for the project.
- **main.py**: The main entry point for the application.

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/Spotify-Instagram-Thing.git
    cd Spotify-Instagram-Thing
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    ```sh
    export CLIENT_ID="your_spotify_client_id"
    export CLIENT_SECRET="your_spotify_client_secret"
    export REDIRECT_URI="http://example.com"
    ```

## Running the Application

To run the application, execute the following command:
```sh
python main.py
```

## Running Tests

To run the tests, use the following command:
```sh
pytest
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## Contact

For any inquiries, please contact [bryan.tran.xyz@gmail.com](mailto:bryan.tran.xyz@gmail.com).