from database.db import get_connection

def verify_email_db(token):
	connection = get_connection()
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM users WHERE verification_token = ?", (token,))
	user = cursor.fetchone()
	if user:
		cursor.execute(
			"UPDATE users SET is_verified = 1, verification_token = NULL WHERE verification_token = ?", (token,)
		)
		connection.commit()
		connection.close()
		return "Email verified successfully!"

	return "Invalid or expired token"