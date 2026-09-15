from pathlib import Path
from rest_framework import serializers
from storage.models import File


class FileSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()
    public_url = serializers.SerializerMethodField()
    owner_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = File
        fields = (
            'id', 'original_name', 'size', 'comment', 'uploaded_at', 'last_downloaded_at',
            'share_token', 'download_url', 'public_url', 'owner_username',
        )
        read_only_fields = ('id', 'size', 'uploaded_at', 'last_downloaded_at', 'share_token', 'download_url', 'public_url', 'owner_username')

    def validate_original_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Имя файла не может быть пустым.')
        if Path(value).name != value or '/' in value or '\\' in value:
            raise serializers.ValidationError('Имя файла не должно содержать путь.')
        return value

    def get_download_url(self, obj):
        path = f'/api/files/{obj.id}/download/'
        request = self.context.get('request')
        return request.build_absolute_uri(path) if request else path

    def get_public_url(self, obj):
        path = f'/share/{obj.share_token}'
        request = self.context.get('request')
        return request.build_absolute_uri(path) if request else path


class PublicFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('original_name', 'size', 'comment')
        read_only_fields = fields
