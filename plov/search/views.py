import elasticsearch_dsl
import rest_framework.response
import rest_framework.views

import stickers.documents


class SearchStickersByText(rest_framework.views.APIView):
    def get(self, request, text):
        q = elasticsearch_dsl.Q(
            'multi_match',
            query=text,
            fields=[
                'decryption',
            ],
            fuzziness='auto',
        )
        search = stickers.documents.StickerDocument.search().query(q)
        response = search.execute()
        return rest_framework.response.Response({'objects': [elem.to_dict() for elem in response]})
