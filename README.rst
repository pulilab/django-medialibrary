medialibrary
========================

Welcome to the documentation for django-medialibrary!


`django-medialibrary` is a pluggable django app that is able to store different media types (audio, video, image) and several versions of a given file in a transparent way.

The basic problam to solve is to store, retrieve and manage several versions of the same file in a seemless way. E.g. a user uploads a video that you will have to transcode into different formats. For the user you would like to show only a single media in his list of uploaded files, but you still want to serve all the generated files when necessary, moreover, if the user decides to delete his media you would like to delete all its versions.

The idea for this app is to have all this in an app-indepedent and easy to use and extend way.

Frontend API
-------------

There is no html frontend on purpose as we are using this app through APIs. The provided APIs out of the box are

``/audio/``, ``/video/``, ``/image/`` - to upload and list media elements of a given type
``/<pk>/`` - to get detailed info about a single media element

Customizations
---------------

Besides the general django settings for file storage, there is a single custom setting, the upload_to method used in the FileFields.::

	import datetime
	def setup_s3_route(instance, filename=None):
	    today = datetime.datetime.today()
	    return 'media/%s-%02d-%02d/%s' % (today.year, today.month, today.day,
	                                          filename)
	from medialibrary import utils 
	utils.setup_upload_route = setup_s3_route

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
