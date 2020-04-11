/* eslint-disable */ module.exports = {
  languageData: {
    plurals: function (n, ord) {
      var s = String(n).split("."),
        v0 = !s[1],
        t0 = Number(s[0]) == n,
        n10 = t0 && s[0].slice(-1),
        n100 = t0 && s[0].slice(-2);
      if (ord)
        return n10 == 1 && n100 != 11
          ? "one"
          : n10 == 2 && n100 != 12
          ? "two"
          : n10 == 3 && n100 != 13
          ? "few"
          : "other";
      return n == 1 && v0 ? "one" : "other";
    },
  },
  messages: {
    "Access-code": "Access-code",
    Action: "Action",
    "All fields are required.": "All fields are required.",
    "An error occurred": "An error occurred",
    "Appointment for the {0}, {1} has been booked": function (a) {
      return ["Appointment for the ", a("0"), ", ", a("1"), " has been booked"];
    },
    "Book Appointment": "Book Appointment",
    "Book appointments": "Book appointments",
    "Booked at": "Booked at",
    "Choose an appointment": "Choose an appointment",
    "Currently <0><1>no Appointments</1></0> are free.":
      "Currently <0><1>no Appointments</1></0> are free.",
    Date: "Date",
    "Date of Appointment": "Date of Appointment",
    "Enter the information for the {0}, {1}": function (a) {
      return ["Enter the information for the ", a("0"), ", ", a("1")];
    },
    Excel: "Excel",
    "Free appointments": "Free appointments",
    From: "From",
    Logout: "Logout",
    "Mobile No.": "Mobile No.",
    "My Appointments": "My Appointments",
    Name: "Name",
    "Notify the patient of the Access-code:":
      "Notify the patient of the Access-code:",
    Print: "Print",
    Surname: "Surname",
    "The appointment is no longer available, please select another free appointment.":
      "The appointment is no longer available, please select another free appointment.",
    "The navigation in the table is possible with Tab and Enter keys.":
      "The navigation in the table is possible with Tab and Enter keys.",
    Timeslot: "Timeslot",
    To: "To",
    "Un unknown error occurred, please reload the page.":
      "Un unknown error occurred, please reload the page.",
    "{coupons, plural, zero {You can book} other {You can still book}}<0><1>{coupons, plural, zero {no appointment} one {{coupons} appointment} other {{coupons} appointments}}</1></0>{coupons, plural, zero {anymore} other {}}": function (
      a
    ) {
      return [
        a("coupons", "plural", {
          zero: "You can book",
          other: "You can still book",
        }),
        " <0><1>",
        a("coupons", "plural", {
          zero: "no appointment",
          one: [a("coupons"), " appointment"],
          other: [a("coupons"), " appointments"],
        }),
        "</1></0> ",
        a("coupons", "plural", { zero: "anymore", other: "" }),
      ];
    },
  },
};
