#!/bin/bash

# Display the menu
echo "Choose an option:"
echo "1. Star Pattern in STAR Shape"
echo "2. Star Pattern in CIRCLE Shape"
read -p "Enter your choice: " choice

# Check if the choice is valid
if [[ "$choice" == "1" || "$choice" == "2" ]]; then
    read -p "Enter the width (odd number for star pattern): " width

    # Ensure width is a positive number
    if ! [[ "$width" =~ ^[0-9]+$ ]] || [ "$width" -le 0 ]; then
        echo "Invalid width. Please enter a positive number."
        exit 1
    fi
fi

case $choice in
    1)  # Star Shape
        echo "Star Pattern in STAR Shape"
        
        # Ensure width is an odd number
        if (( width % 2 == 0 )); then
            echo "Only enter an odd number for star pattern."
            exit 1
        fi

        # Generate the star pattern
        n=$width  # `n` is the width (odd number)
        for ((i = 0; i < n; i++)); do # Rows
            for ((j = 0; j < n; j++)); do # Columns
                if [ $i -eq $((n / 2)) ] || [ $j -eq $((n / 2)) ] || # Middle row and column
                   { [ $i -eq $j ] && [ $i -le $((n / 2)) ]; } ||  # Top-left diagonal
                   { [ $((i + j)) -eq $((n - 1)) ] && [ $i -le $((n / 2)) ]; } || # Top-right diagonal
                   { [ $i -eq $j ] && [ $i -ge $((n / 2)) ]; } ||  # Bottom-left diagonal
                   { [ $((i + j)) -eq $((n - 1)) ] && [ $i -ge $((n / 2)) ]; }; then # Bottom-right diagonal
                    echo -n "*"
                else
                    echo -n " "
                fi
            done
            echo
        done
    ;;

    2)  # Circle Shape
        echo "Star Pattern in CIRCLE Shape"

        # Set the radius of the circle based on width (Diameter)
        radius=$((width / 2))

        # Loop through y-coordinates
        for ((y = -radius; y <= radius; y++)); do
            # Loop through x-coordinates
            for ((x = -radius; x <= radius; x++)); do
                # Equation for a circle: x^2 + y^2 <= r^2
                if (( x*x + y*y <= radius*radius )); then
                    echo -n "*"
                else
                    echo -n " "
                fi
            done
            echo # Move to the next line after finishing one row
        done
    ;;
    
    *)
        echo "Invalid choice"
    ;;
esac
