# -*- coding: utf-8 -*-

from server.skeleton import Skeleton
from server.bones import *
from server import conf, utils

from collections import OrderedDict

class regSkel(Skeleton):
	subSkels = {"restricted": ["key", #"viewname", "firstname", "lastname", #DSGVO 2018
							   	"aircraft", "aircraft_ignore", "aircraft_type", "aircraft_reg",
	                            "aircraft_wb", "aircraft_pic", "aircraft_pic_ok", "aircraft_werkno",
	                            "aircraft_bj", "creationdate", "club", "visible", "persons", "slideshow"],
				"regform": ["email", "title", "viewname", "firstname", "lastname", "club", "city",
	                        "phone", "persons", "camping", "camping_kind",
	                        "aircraft", "aircraft_type", "aircraft_reg",
	                        "aircraft_wb", "aircraft_pic", "aircraft_title",
	                        "aircraft_transport", "remarks", "creationdate", "changedate",
				            "aircraft_flight", "aircraft_others", "aircraft_others_comment",
				            "aircraft_nightup", "aircraft_bj", "aircraft_werkno",
				            "vegetarier", "tag_*", "tshirt_*", "sweatshirt_*", "tasse_*", "cap_*",
				            "frameprog", "qremarks", "code", "questionaire_*", "nomail", "slideshow",
							"accept_*"]}

	email = emailBone(
		descr=u"E-Mail Adresse",
		indexed=True,
		searchable=True,
		required=True,
		unique=u"Diese E-Mail Adresse wird bereits verwendet!")

	title = selectBone(
		descr=u"Anrede",
		required=True,
		values={"m": u"Herr", "f": u"Frau"}
	)
	viewname = stringBone(
		descr=u"Anzeigename",
		searchable=True
	)
	firstname = stringBone(
		descr=u"Vorname",
		required=True,
		indexed=True,
		searchable=True
	)
	lastname = stringBone(
		descr=u"Nachname",
		required=True,
		indexed=True,
		searchable=True
	)
	club = stringBone(
		descr=u"Heimatverein",
		indexed=True,
		searchable=True
	)

	street = stringBone(
		descr=u"Anschrift",
		required=False,
		indexed=True,
		searchable=True
	)

	zipcode = stringBone(
		descr=u"PLZ",
		required=False,
		indexed=True,
		searchable=True
	)
	city = stringBone(
		descr=u"Stadt",
		indexed=True,
		searchable=True
	)

	country = selectCountryBone(
		descr=u"Land",
		required=False,
		defaultValue="de",
		indexed=True
	)

	phone = stringBone(descr=u"Telefon", indexed=True, searchable=True)

	persons = numericBone(descr=u"Personenanzahl", min=1, max=9, defaultValue=1)
	vegetarier = numericBone(descr=u"Anzahl Vegetarier", defaultValue=0, indexed=True)

	# Camping
	camping = booleanBone(descr=u"Camping", params={"category": u"Camping"}, defaultValue=False)
	camping_kind = selectBone(descr=u"Camping-Art",
	                                values={"tent": "Zelt",
	                                        "caravan": "Wohnmobil/Wohnwagen"},
	                                params={"category": u"Camping"})

	# Flugzeug
	aircraft = booleanBone(
		descr=u"Mit Flugzeug?",
		params={"category": u"Flugzeug"},
		indexed=True,
		defaultValue=False
	)

	aircraft_ignore = booleanBone(
		descr=u"Flugzeug ignorieren",
		params={"category": u"Flugzeug"},
		indexed=True,
		defaultValue=False
	)

	aircraft_type = selectBone(
		descr=u"Flugzeugtyp",
		params={"category": u"Flugzeug"},
	    indexed=True,
		searchable=True,
		values=OrderedDict(
			[(i, v) for i, v in enumerate([
				u"H-30 GFK",
				u"H-301 Libelle",
				u"BS-1",
				u"Standard Libelle 201",
				u"Kestrel 401",
				u"Standard Libelle 202",
				u"Standard Libelle 203",
				u"Standard Libelle 204",
				u"Club Libelle 205",
				u"Hornet 206",
				u"Hornet C",
				u"Mosquito 303",
				u"Glasflügel 304",
				u"Glasflügel 402",
				u"Falcon",
				u"start+flug H-101 Salto",
				u"start+flug H-111 Hippie"
			])
		])
	)

	aircraft_reg = stringBone(
		descr=u"Kennzeichen",
		params={"category": u"Flugzeug"},
	    indexed=True,
		searchable=True
	)
	aircraft_wb = stringBone(
		descr=u"WB-Kennzeichen",
		params={"category": u"Flugzeug"},
	    indexed=True,
		searchable=True
	)
	aircraft_bj = stringBone(
		descr=u"Baujahr",
		params={"category": u"Flugzeug"}
	)
	aircraft_werkno = stringBone(
		descr=u"Werk-Nr.",
		params={"category": u"Flugzeug"}
	)

	aircraft_pic = fileBone(
		descr=u"Galeriebild",
		params={"category": u"Flugzeug"}
	)
	aircraft_pic_ok = booleanBone(
		descr=u"Bild geprüft und sichtbar?",
	    params={"category": u"Flugzeug"},
	    indexed=True,
	    defaultValue=False
	)
	aircraft_transport = selectBone(
		descr=u"Transport",
	    values={"trailer": "Trailer", "flight": "per Luft"},
		params={"category": u"Flugzeug"})

	# Wettbewerb
	accept_wb = booleanBone(
		descr=u"Wettbewerbsordnung akzeptiert",
		indexed=True,
		defaultValue=False
	)

	accept_dsgvo = booleanBone(
		descr=u"Datenschutzvereinbarung akzeptiert",
		indexed=True,
		defaultValue=False
	)

	# Fragebogen
	aircraft_flight = selectBone(descr=u"Möchte fliegen?", values={"1": "Ja", "0": "Nein", "-": "Vielleicht"},
	                                defaultValue="1", params={"category": u"Flugzeug"})
	aircraft_others = booleanBone(descr=u"Typenfliegen", defaultValue=False, params={"category": u"Flugzeug"})
	aircraft_others_comment = stringBone(descr=u"Typenfliegen Bemerkung", params={"category": u"Flugzeug"})
	aircraft_nightup = booleanBone(descr=u"Typenfliegen", defaultValue=False, params={"category": u"Flugzeug"})

	tag_fr = booleanBone(descr=u"Freitag", indexed=True, defaultValue=False, params={"category": u"Anwesenheit"})
	tag_sa = booleanBone(descr=u"Samstag", indexed=True, defaultValue=True, readOnly=True, params={"category": u"Anwesenheit"})
	tag_so = booleanBone(descr=u"Sonntag", indexed=True, defaultValue=False, params={"category": u"Anwesenheit"})


	tshirt_flyin_white_xs = numericBone(descr=u"FLYIN T-Shirt XS hell", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tshirt_flyin_white_s = numericBone(descr=u"FLYIN T-Shirt S hell", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tshirt_flyin_white_m = numericBone(descr=u"FLYIN T-Shirt M hell", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tshirt_flyin_white_l = numericBone(descr=u"FLYIN T-Shirt L hell", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tshirt_flyin_white_xl = numericBone(descr=u"FLYIN T-Shirt XL hell", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tshirt_flyin_white_xxl = numericBone(descr=u"FLYIN T-Shirt XXL hell", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tshirt_flyin_black_xs = numericBone(descr=u"FLYIN T-Shirt XS dunkel", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tshirt_flyin_black_s = numericBone(descr=u"FLYIN T-Shirt S dunkel", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tshirt_flyin_black_m = numericBone(descr=u"FLYIN T-Shirt M dunkel", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tshirt_flyin_black_l = numericBone(descr=u"FLYIN T-Shirt L dunkel", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tshirt_flyin_black_xl = numericBone(descr=u"FLYIN T-Shirt XL dunkel", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tshirt_flyin_black_xxl = numericBone(descr=u"FLYIN T-Shirt XXL dunkel", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})

	tshirt_logo_white_xs = numericBone(descr=u"LOGO T-Shirt XS hell", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tshirt_logo_white_s = numericBone(descr=u"LOGO T-Shirt S hell", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tshirt_logo_white_m = numericBone(descr=u"LOGO T-Shirt M hell", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tshirt_logo_white_l = numericBone(descr=u"LOGO T-Shirt L hell", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tshirt_logo_white_xl = numericBone(descr=u"LOGO T-Shirt XL hell", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tshirt_logo_white_xxl = numericBone(descr=u"LOGO T-Shirt XXL hell", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tshirt_logo_black_xs = numericBone(descr=u"LOGO T-Shirt XS dunkel", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tshirt_logo_black_s = numericBone(descr=u"LOGO T-Shirt S dunkel", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tshirt_logo_black_m = numericBone(descr=u"LOGO T-Shirt M dunkel", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tshirt_logo_black_l = numericBone(descr=u"LOGO T-Shirt L dunkel", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tshirt_logo_black_xl = numericBone(descr=u"LOGO T-Shirt XL dunkel", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tshirt_logo_black_xxl = numericBone(descr=u"LOGO T-Shirt XXL dunkel", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})

	sweatshirt_white_xs = numericBone(descr=u"Sweatshirt T-Shirt XS hell", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	sweatshirt_white_s = numericBone(descr=u"Sweatshirt T-Shirt S hell", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	sweatshirt_white_m = numericBone(descr=u"Sweatshirt T-Shirt M hell", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	sweatshirt_white_l = numericBone(descr=u"Sweatshirt T-Shirt L hell", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	sweatshirt_white_xl = numericBone(descr=u"Sweatshirt T-Shirt XL hell", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	sweatshirt_white_xxl = numericBone(descr=u"Sweatshirt T-Shirt XXL hell", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	sweatshirt_black_xs = numericBone(descr=u"Sweatshirt T-Shirt XS dunkel", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	sweatshirt_black_s = numericBone(descr=u"Sweatshirt T-Shirt S dunkel", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	sweatshirt_black_m = numericBone(descr=u"Sweatshirt T-Shirt M dunkel", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	sweatshirt_black_l = numericBone(descr=u"Sweatshirt T-Shirt L dunkel", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	sweatshirt_black_xl = numericBone(descr=u"Sweatshirt T-Shirt XL dunkel", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	sweatshirt_black_xxl = numericBone(descr=u"Sweatshirt T-Shirt XXL dunkel", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})

	tasse_h30 = numericBone(descr=u"Tasse H-30", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tasse_301 = numericBone(descr=u"Tasse Libelle H-301", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tasse_bs1 = numericBone(descr=u"Tasse BS-1", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tasse_201 = numericBone(descr=u"Tasse Libelle 201b", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tasse_kestrel = numericBone(descr=u"Tasse Kestrel", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tasse_604 = numericBone(descr=u"Tasse 604", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tasse_clubby = numericBone(descr=u"Tasse Clublibelle", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tasse_hornet = numericBone(descr=u"Tasse Hornet", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tasse_mosquito = numericBone(descr=u"Tasse Mosquito", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tasse_304 = numericBone(descr=u"Tasse 304", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tasse_falcon = numericBone(descr=u"Tasse Falcon", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})
	tasse_402 = numericBone(descr=u"Tasse 402", defaultValue=0, indexed=True, params={"category": u"Fragebogen"})

	cap_white = numericBone(descr=u"Glasflügel Cap, hell", defaultValue=0, indexed=True,
	                        params={"category": u"Fragebogen"})
	cap_black = numericBone(descr=u"Glasflügel Cap, dunkel", defaultValue=0, indexed=True,
	                        params={"category": u"Fragebogen"})

	# Sonstiges
	frameprog = textBone(descr=u"Rahmenprogramm")
	remarks = textBone(descr=u"Bemerkungen")
	qremarks = textBone(descr=u"Was ich unbedingt noch loswerden möchte")
	visible = booleanBone(descr=u"Sichtbar", indexed=True, defaultValue=False)

	questionaire_sent = booleanBone(descr=u"Fragebogen erhalten", defaultValue=False, indexed=True)
	questionaire_filled = booleanBone(descr=u"Fragebogen ausgefüllt", defaultValue=False, indexed=True)

	code = stringBone(descr=U"Bearbeitungscode", readOnly=True)

	nomail = booleanBone(descr=u"Keine E-Mails an Teilnehmer versenden", defaultValue=False)

	slideshow = booleanBone(descr=u"Slideshow", defaultValue=False, indexed=True)

	def toDB(self, *args, **kwargs):
		if "viewname" in self.keys():
			if not self["viewname"]:
				self["viewname"] = "%s %s" % (self["firstname"], self["lastname"])

		if "code" in self.keys() and not self["code"]:
			self["code"] = utils.generateRandomString()

		#if "slideshow" in self.keys():
		#	self["slideshow"].value = self["visible"].value and self["aircraft_pic_ok"].value and not self["aircraft_ignore"].value

		return super(regSkel, self).toDB(*args, **kwargs)
