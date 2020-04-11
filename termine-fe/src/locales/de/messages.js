/* eslint-disable */ module.exports = {
  languageData: {
    plurals: function (n, ord) {
      var s = String(n).split("."),
        v0 = !s[1];
      if (ord) return "other";
      return n == 1 && v0 ? "one" : "other";
    },
  },
  messages: {
    "Access-code": "Berechtigungscode",
    Action: "Aktion",
    "All fields are required.": "Alle Felder sind Pflichtfelder.",
    "An error occurred": "Es ist ein Fehler aufgetreten",
    "Appointment for the {0}, {1} has been booked": function (a) {
      return ["Termin f\xFCr den ", a("0"), ", ", a("1"), " wurde gebucht"];
    },
    "Book Appointment": "Termin Buchen",
    "Book appointments": "Termine Buchen",
    "Booked at": "Gebucht am",
    "Choose an appointment": "W\xE4hlen Sie einen Termin aus",
    "Currently <0><1>no Appointments</1></0> are free.":
      "Aktuell sind <0><1>keine Termine</1></0> mehr frei.",
    Date: "Datum",
    "Date of Appointment": "Datum des Termins",
    "Enter the information for the {0}, {1}": function (a) {
      return ["Tragen Sie die Daten f\xFCr den ", a("0"), ", ", a("1"), " ein"];
    },
    Excel: "Excel",
    "Free appointments": "Freie Termine",
    From: "Von",
    Logout: "Logout",
    "Mobile No.": "Handynummer",
    "My Appointments": "Meine Buchungen",
    Name: "Vorname",
    "Notify the patient of the Access-code:":
      "Teilen Sie dem Patienten jetzt den Berechtigungscode mit:",
    Print: "Drucken",
    Surname: "Nachname",
    "The appointment is no longer available, please select another free appointment.":
      "Leider ist der Termin inzwischen nicht mehr buchbar, bitte einen anderen Termin w\xE4hlen.",
    "The navigation in the table is possible with Tab and Enter keys.":
      "In der Tabelle kann mit Tab und Enter navigiert werden.",
    Timeslot: "Terminslot",
    To: "Bis",
    "Un unknown error occurred, please reload the page.":
      "Ein unbekannter Fehler ist aufgetreten, bitte Seite neu laden.",
    "{coupons, plural, zero {You can book} other {You can still book}}<0><1>{coupons, plural, zero {no appointment} one {{coupons} appointment} other {{coupons} appointments}}</1></0>{coupons, plural, zero {anymore} other {}}": function (
      a
    ) {
      return [
        a("coupons", "plural", {
          zero: "Sie k\xF6nnen",
          other: "Sie k\xF6nnen noch",
        }),
        " <0><1>",
        a("coupons", "plural", {
          zero: "keinen Termin",
          one: "einen Termin",
          other: [a("coupons"), " Termine"],
        }),
        "</1></0> ",
        a("coupons", "plural", { zero: "mehr buchen", other: "buchen" }),
      ];
    },
  },
};
