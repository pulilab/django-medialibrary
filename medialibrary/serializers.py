from rest_framework import serializers
from .models import Audio, Image, Video, AudioShelf, ImageShelf, VideoShelf

def basefileserializer_factory(mymodel):

    class ThisClass(serializers.ModelSerializer):
        # imagefile = serializers.ImageField()
        # thumbnail = serializers.SerializerMethodField('get_thumbnail_url')
        url = serializers.SerializerMethodField('get_file_url')

        class Meta:
            model = mymodel
            fields = ('file', 'descriptor', 'meta', 'url')

        def get_thumbnail_url(self, obj):
            return obj.imagefile.thumb.url

        def get_file_url(self, obj):
            return obj.file.url

    return ThisClass

ImageSerializer = basefileserializer_factory( Image )
AudioSerializer = basefileserializer_factory( Audio )
VideoSerializer = basefileserializer_factory( Video )

basefileserializer_registry = {
    'image': ImageSerializer,
    'audio': AudioSerializer,
    'video': VideoSerializer,
}

class ShelfSerializer(serializers.ModelSerializer):

    library = serializers.PrimaryKeyRelatedField(required=True, many=False)
    url = serializers.Field(source='get_absolute_url')

    def __init__(self, *args, **kwargs):
        self.shelf_type = kwargs['context'].get('shelf_type', None)
        method = kwargs['context'].get('method', None)

        if not self.shelf_type:
            raise ValueError('Shelf type must be specified in the ShelfSerializer context')

        if kwargs.get('files', None) and len( kwargs['files'].keys() ) > 1:
            raise ValueError('Only a single file can be uploaded at a time')            

        shelf_types = {
            'image': ImageShelf,
            'audio': AudioShelf,
            'video': VideoShelf,
        }

        self.Meta.model = shelf_types[self.shelf_type]

        super(ShelfSerializer, self).__init__(*args, **kwargs)

        if method == 'POST':  #: we are creating a shelve
            self.file_serializer = basefileserializer_registry[self.shelf_type](
                data={}, files=kwargs.pop('files')
            )
        elif method == 'PUT':  #: we are updating a shelve
            files = serializers.PrimaryKeyRelatedField(
                source='%s_set.add' % self.shelf_type, 
                required=True, many=False
            )
        else:
            self.fields['%s_set' % self.shelf_type] = basefileserializer_registry[self.shelf_type](many=True)
            self.fields['files'] = serializers.SerializerMethodField('get_files')

    def validate(self, data):
        if not self.file_serializer.is_valid():
            raise serializers.ValidationError("The attached file did not validate: %s" % str(self.file_serializer.errors))
        return data

    def save_file(self, shelf):
        self.file_serializer.object.shelf = shelf
        newfile = self.file_serializer.save()
        return newfile

    def save(self, **kwargs):
        shelf = super(ShelfSerializer, self).save()
        self.save_file(shelf)
        return shelf

    def get_files(self, obj):
        return getattr(self, '%s_set' % self.shelf_type, [])

    def to_native(self, obj):
        """As get_files usually evaluates to [], we add its value here as well"""
        data = super(ShelfSerializer, self).to_native(obj)
        if data.has_key('files') and not data['files']:
            data['files'] = data['%s_set' % self.shelf_type]
        return data

    class Meta:
        fields = ('url', 'name', 'state', 'library')
        read_only_fields = ('state', )

