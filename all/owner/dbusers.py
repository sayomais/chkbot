from all.configs._def_main_ import *
import csv
import os
import logging

# Configure logging to debug issues
logging.basicConfig(level=logging.DEBUG)

@Techie('userp')
async def userinfocmd(_, message):
    try:
        # Fetch user permissions
        permisos = collection.find_one({"_id": message.from_user.id})
        if not permisos:
            logging.warning(f"No permissions found for user: {message.from_user.id}")
            return
        
        # Check if user is Owner
        if permisos.get('role') == "Owner":
            logging.debug(f"User {message.from_user.id} has 'Owner' role. Proceeding.")
            
            # Fetch premium users
            premium_users = collection.find({
                "$or": [
                    {"plan": "Premium"},
                    {"role": "Seller"},
                    {"role": "Owner"}
                ]
            })
            
            # Generate a unique filename for the CSV to avoid conflicts
            filename = f'premium_users_{message.from_user.id}.csv'

            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                # Define CSV column headers
                fieldnames = ['ID', 'Username', 'Plan', 'Status', 'Key']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

                # Write user data to the CSV
                for user in premium_users:
                    writer.writerow({
                        'ID': user.get('_id', ''),
                        'Username': user.get('username', ''),
                        'Plan': user.get('plan', ''),
                        'Status': user.get('status', ''),
                        'Key': user.get('key', '')
                    })

            logging.debug(f"CSV file '{filename}' created successfully.")

            # Send the CSV file to the user
            await message.reply_document(document=filename, quote=True)
            logging.debug(f"CSV file '{filename}' sent to user {message.from_user.id}.")
            
            # Remove the file after sending it
            os.remove(filename)
            logging.debug(f"CSV file '{filename}' removed from server.")

        else:
            logging.warning(f"User {message.from_user.id} does not have sufficient permissions.")
            return

    except Exception as e:
        # Log any errors
        logging.error(f"An error occurred: {e}")
        await message.reply_text(f"An error occurred: {str(e)}", quote=True)
