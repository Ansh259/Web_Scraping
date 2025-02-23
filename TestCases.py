import pytest
from unittest.mock import patch
from My_Program.py import parse_data, generate_excel, save_html_to_zip  
import os
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('Excel Read').gerOrCreate()

# Mock data to simulate the parsed HTML data
mock_html_data = [
    """
    <table>
        <tr><th>Team</th><th>Year</th><th>Wins</th><th>Losses</th><th>OT Losses</th><th>Win %</th><th>Goals For(GF)</th><th>Goals Against(GA)</th><th>+/-</th></tr>
        <tr><td>Team A</td><td>1990</td><td>50</td><td>30</td><td>2</td><td>0.600</td><td>200</td><td>180</td><td>20</td></tr>
        <tr><td>Team B</td><td>1990</td><td>40</td><td>40</td><td>4</td><td>0.500</td><td>190</td><td>190</td><td>0</td></tr>
    </table>
    """,
    """
    <table>
        <tr><th>Team</th><th>Year</th><th>Wins</th><th>Losses</th><th>OT Losses</th><th>Win %</th><th>Goals For(GF)</th><th>Goals Against(GA)</th><th>+/-</th></tr>
        <tr><td>Team C</td><td>1991</td><td>55</td><td>25</td><td>3</td><td>0.650</td><td>210</td><td>170</td><td>40</td></tr>
        <tr><td>Team D</td><td>1991</td><td>30</td><td>50</td><td>4</td><td>0.400</td><td>180</td><td>210</td><td>-30</td></tr>
    </table>
    """
]

# Test the parse_data function to ensure it processes mock HTML data correctly
def test_parse_data():
    # Call parse_data with the mock HTML data
    stats = parse_data(mock_html_data)

    # Assert the length of parsed data
    assert len(stats) == 4

    # Test a sample value from the parsed data
    assert stats[0]['Team Name'] == 'Team A'
    assert stats[0]['Wins'] == 50
    assert stats[0]['Losses'] == 30
    assert stats[0]['Win %'] == 0.600

    # Test a sample value from another team
    assert stats[2]['Team Name'] == 'Team C'
    assert stats[2]['Year'] == '1991'
    assert stats[2]['+/-'] == 40

# Test the Excel generation (without actually saving to a file, use mocking)
def test_generate_excel():
    stats = parse_data(mock_html_data)

    # Mock the saving of the Excel file (no actual file will be created)
    with patch('openpyxl.Workbook.save') as mock_save:
        generate_excel(stats)
        mock_save.assert_called_once()  # Ensure save was called once

# Test the save_html_to_zip function (mocking file operations)
def test_save_html_to_zip():
    with patch('zipfile.ZipFile') as mock_zip:
        # Mock the 'write' method of the ZipFile object
        mock_zip_instance = mock_zip.return_value.__enter__.return_value
        with patch('builtins.open', unittest.mock.mock_open()) as mock_open:
            save_html_to_zip(mock_html_data)

            # Ensure the 'write' method was called (which simulates saving the files)
            mock_zip_instance.write.assert_called()
            mock_open.assert_called()

# Test the generated Excel file content using pandas (mocked)
def test_excel_content():
    stats = parse_data(mock_html_data)
    with patch('openpyxl.Workbook.save') as mock_save:
        generate_excel(stats)

    # Read the generated Excel file using pandas to check content
    df = spark.read.format("xlsx").option("header","true").load('hockey_stats.xlsx')
    df.show()

    # Check if the first few rows match expected values
    assert df.iloc[0]['Team Name'] == 'Team A'
    assert df.iloc[0]['Wins'] == 50
    assert df.iloc[0]['Year'] == '1990'
    assert df.iloc[2]['+/-'] == 40

# Test the output ZIP file content
def test_zip_content():
    # Let's mock the `zipfile.ZipFile` class
    with patch('zipfile.ZipFile') as mock_zip:
        mock_zip_instance = mock_zip.return_value.__enter__.return_value
        save_html_to_zip(mock_html_data)

        # Assert that 'write' was called on the zip instance
        mock_zip_instance.write.assert_called()

        # Check the expected file names inside the ZIP (you can adjust this based on your naming convention)
        mock_zip_instance.write.assert_any_call('1.html')
        mock_zip_instance.write.assert_any_call('2.html')
