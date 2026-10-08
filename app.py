from flask import Flask, render_template, request
from datetime import date


def validate_registration(form, files):
    # Client-side validation improves user experience, but the client is
    # untrusted and can be modified or bypassed. We deliberately duplicate
    # the validation rules on the server because the server is the trust boundary.

    errors = {}

    # Name
    name = form.get("name", "").strip()

    if not name:
        errors["name"] = "Name is required."
    elif len(name) < 3 or len(name) > 25:
        errors["name"] = "Name must be between 3 and 25 characters."

    # Email
    email = form.get("email", "").strip()

    if not email:
        errors["email"] = "Email is required."
    elif len(email) > 100:
        errors["email"] = "Email must not exceed 100 characters."
    elif "@" not in email:
        errors["email"] = "Please enter a valid email address."

    # Password
    password = form.get("password", "")

    if not password:
        errors["password"] = "Password is required."
    elif len(password) < 8 or len(password) > 64:
        errors["password"] = "Password must be between 8 and 64 characters."

    # Phone
    phone = form.get("phone", "").strip()

    if not phone:
        errors["phone"] = "Phone number is required."
    elif len(phone) != 10 or not phone.isdigit():
        errors["phone"] = "Phone number must contain exactly 10 digits."

    # Age
    age = form.get("age", "").strip()

    if not age:
        errors["age"] = "Age is required."
    else:
        try:
            age = int(age)

            if age < 18 or age > 25:
                errors["age"] = "Age must be between 18 and 25."

        except ValueError:
            errors["age"] = "Age must be a valid number."

    # Date of birth
    dob = form.get("dob", "").strip()

    if not dob:
        errors["dob"] = "Date of birth is required."
    else:
        try:
            dob_date = date.fromisoformat(dob)

            today = date.today()

            calculated_age = today.year - dob_date.year

            if (today.month, today.day) < (dob_date.month, dob_date.day):
                calculated_age -= 1

            if calculated_age < 18 or calculated_age > 25:
                errors["dob"] = (
                    "Age calculated from date of birth must be between 18 and 25."
                )

        except ValueError:
            errors["dob"] = "Date of birth must be a valid date."

    # Gender
    gender = form.get("gender", "").strip()

    allowed_genders = {"male", "female", "others"}

    if not gender:
        errors["gender"] = "Gender is required."
    elif gender not in allowed_genders:
        errors["gender"] = "Invalid gender value."

    # Skills
    skills = form.getlist("skills")

    allowed_skills = {"html", "css", "javascript", "python"}

    if not skills:
        errors["skills"] = "Select at least one skill."
    elif any(skill not in allowed_skills for skill in skills):
        errors["skills"] = "Invalid skill selected."

    # Terms and conditions
    terms = form.get("terms")

    if terms != "accepted":
        errors["terms"] = "You must accept the terms and conditions."

    # Hidden field tamper protection
    form_version = form.get("form_version")

    if form_version != "1":
        errors["form_version"] = "Invalid form version."

    # Profile photo
    profile = files.get("profile")

    if profile and profile.filename:
        allowed_extensions = {".jpg", ".jpeg", ".png"}
        filename = profile.filename.lower()

        if not any(filename.endswith(ext) for ext in allowed_extensions):
            errors["profile"] = "Only JPG, JPEG, and PNG files are allowed."

        MAX_FILE_SIZE = 2 * 1024 * 1024

        profile.seek(0, 2)
        file_size = profile.tell()
        profile.seek(0)

        if file_size > MAX_FILE_SIZE:
            errors["profile"] = "Profile photo must not exceed 2 MB."

    return errors


app = Flask(__name__)


@app.route("/")
def register():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def submit_registration():
    errors = validate_registration(request.form, request.files)

    if errors:
        return errors, 400

    return render_template("result.html", name=request.form.get("name"))


if __name__ == "__main__":
    app.run(debug=True)
