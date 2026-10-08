## Security Self-Tests

The following tests were performed to verify that client-side validation cannot be trusted as the only security measure.

### 1. JavaScript Disabled

JavaScript was disabled and invalid data was submitted.

**Result:** Native HTML validation continued to work for fields such as required fields, length limits, input types, and numeric ranges. The custom JavaScript validation for the skills checkbox group was bypassed, but the Flask server rejected the submission because no skill was selected.

**Conclusion:** Server-side validation protects the application even when JavaScript is disabled.

---

### 2. Client-Side Validation Modified Using DevTools

The `required` attribute was removed from the Name field using browser DevTools and an empty name was submitted.

**Result:** The browser allowed the submission, but the Flask server rejected it with:

`Name is required.`

The `maxlength` value was also modified and a name longer than the server limit was submitted.

**Result:** The Flask server rejected the value with:

`Name must be between 3 and 25 characters.`

**Conclusion:** Client-side validation rules can be modified by users, so server-side validation is necessary.

---

### 3. Hidden Field Tampering

The hidden `form_version` field was changed from `1` to another value using DevTools.

**Result:** The server rejected the request with:

`Invalid form version.`

**Conclusion:** Hidden fields are not trusted because users can modify them.

---

### 4. Direct POST Request Using curl

A POST request containing multiple invalid values was sent directly to the Flask `/register` endpoint using curl, without using the browser form.

**Result:** The server returned HTTP `400 Bad Request` and rejected the invalid fields.

**Conclusion:** The server validates incoming data independently of the browser and cannot be bypassed simply by avoiding the HTML form.

---

### 5. Cross-Site Scripting (XSS)

The following value was submitted as the name:

`<script>alert(1)</script>`

The submitted name was displayed back by the application.

**Result:** The script did not execute. It was displayed as text.

**Fix:** User-controlled data is rendered using normal Jinja2 template escaping:

`{{ name }}`

The unsafe `|safe` filter is not used for user-controlled input.

**Conclusion:** Jinja2's automatic HTML escaping prevents the submitted script from being interpreted as executable JavaScript.