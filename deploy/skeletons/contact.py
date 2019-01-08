# -*- coding: utf-8 -*-
from server.skeleton import Skeleton
from server.bones import *

class contactSkel(Skeleton):
	entityName = None
	key = None

	email= emailBone(descr="E-Mail", required=True)
	descr = textBone(descr="Nachricht", required=True)

	privacy_confirm = booleanBone(descr=u"Ich bin damit einverstanden, dass meine angegebenen Daten zum Zwecke der Bearbeitung der Anfrage gespeichert und weiterverarbeitet werden dürfen. Eine Übermittlung meiner Daten an Dritte findet nicht statt.", required=True)
