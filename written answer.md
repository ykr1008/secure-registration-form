A candidate tells me their form is secure because it validates everything on the client. I would explain that client-side validation is useful for usability, but it is not a security boundary. The user has complete control over the browser and can modify the HTML, disable JavaScript, change validation attributes, or completely bypass the form and send a request directly to the server.

For example, a user can remove a required attribute or change a maxlength value using browser DevTools. They can also send a manually crafted POST request using tools such as curl or Postman. Therefore, any validation performed only in HTML or JavaScript can be bypassed.

The server must independently validate every piece of data it receives. This includes checking required fields, lengths, allowed values, numeric ranges, dates, uploaded files, checkbox values, and hidden fields. The server should treat all client-provided data as untrusted, including hidden inputs because hidden fields can also be modified.

Client-side validation should still be used because it provides immediate feedback and improves the user experience. However, it should be considered a convenience rather than a security mechanism.

Output handling is also important. If user-controlled data is displayed back on a page, it must be safely escaped to prevent attacks such as cross-site scripting (XSS). In Flask, Jinja2 normally escapes variables rendered with {{ value }}, so untrusted input should not be marked as safe.

In short, the browser can help validate input, but only the server can enforce security rules. A secure application therefore validates untrusted data on the server and safely handles it when displaying it back to users.