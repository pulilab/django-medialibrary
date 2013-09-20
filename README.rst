Medialibrary for Django
========================

Welcome to the documentation for django-medialibrary!


`django-medialibrary` is a pluggable django app that is able to store different media types (audio, video, image) and several versions of a given file in a transparent way.

The basic problam to solve is to store, retrieve and manage several versions of the same file in a seemless way. E.g. a user uploads a video that you will have to transcode into different formats. For the user you would like to show only a single media in his list of uploaded files, but you still want to serve all the generated files when necessary, moreover, if the user decides to delete his media you would like to delete all its versions.

The idea for this app is to have all this in an app-indepedent and easy to use and extend way.

Features
---------

* Unique entry point for every media type, `user.medialibrary.shelf_set`
* Different shelfs with possible different login for every media type. The `shelf_set` contains different models, each derived from `medialibrary.models.Shelf`.
* Simple access to the original file.::

	myShelf = AudioShelf.objects.get(pk=1)
	myShelf.audio_set.all()  # returns the list of audio files
	isinstance(myShelf.original, Audio)  # return True, if a file is attached to myShelf
	myShelf.original.size, myShelf.original.url

* Custom manager to query the shelves.
* Generic relationships to bind the shelves to any object in the project, using the ShelfRelation model
* Every shelf type can have an ALLOWED_FORMATS property that lists the allowed extensions to be save in the shelf.
* VideoShelves can have thumbnail images (actually ImageShelf instances) attached. Only one of these can be marked as selected. The myVideoShelf.thumbnail property returns the selected thumbnail.


Frontend API
-------------

There is no html frontend on purpose as we are using this app through APIs. The provided APIs out of the box are

* ``/audio/``, ``/video/``, ``/image/`` - to upload and list media elements of a given type
* ``/<pk>/`` - to get detailed info about a single media element
* ``/<pk>/add/`` - adds a relationship to the media element, expects a json of the form::

	{
		'model': 'app_name.model_name',
		'object_id': 1
	}

where ``app_name.model_name`` is the `natural key <https://docs.djangoproject.com/en/1.5/topics/serialization/#topics-serialization-natural-keys>`_ of the model you are attaching.

Customizations
---------------

Besides the general django settings for file storage, there is a custom setting, the upload_to method used in the FileFields.::

	import datetime
	def setup_s3_route(instance, filename=None):
	    today = datetime.datetime.today()
	    return 'media/%s-%02d-%02d/%s' % (today.year, today.month, today.day,
	                                          filename)
	from medialibrary import utils 
	utils.setup_upload_route = setup_s3_route

You can set a custom argument for the ``limit_choices_to`` attribute on the ShelfRelation model. This way you can define which apps are allowed to have relationships to you media elements. (e.g. if you remove the attached records when you remove the media, you probably don't want to attach django permission records to media). The default is **no restricions**!::

	from medialibrary import utils
	from django.db import models
	utils.content_type_restriction = models.Q(app_label='auth', model='user')

Adding new media types
_______________________

The medialibrary can be easily extended with new media types. Here is an example to add a new DocumentShelf model::

	from medialibrary.models import Shelf

	class DocumentShelf(Shelf):

	    ALLOWED_FORMATS = ('doc', 'docx', 'pdf', 'odf')

	    def file_set():
	        doc = "The file_set property."
	        def fget(self):
	            return self.audio_set
	        return locals()
	    file_set = property(**file_set())

After this simple model definition, the user's `user.medialibrary.shelf_set` will contain DocumentShelf instances whenever appropriate. 

Installation
-------------

``pip install django-medialibrary``

or you can `find the project on github <https://github.com/pulilab/django-medialibrary>`_

Running the Tests
------------------------------------

You can run the tests with via::

    python setup.py test

or::

    python runtests.py

Sponsors
----------

This app was written at `Pulilab <http://pulilab.com>`_ while we were working on `Vidzor <http://vidzor.com>`_.
