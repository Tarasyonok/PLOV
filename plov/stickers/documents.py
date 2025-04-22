import django_elasticsearch_dsl
import django_elasticsearch_dsl.registries

import stickers.models


@django_elasticsearch_dsl.registries.registry.register_document
class StickerDocument(django_elasticsearch_dsl.Document):
    id = django_elasticsearch_dsl.fields.IntegerField()

    class Index:
        name = 'text_on_sticker'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = stickers.models.Sticker
        fields = [
            'decryption',
        ]
