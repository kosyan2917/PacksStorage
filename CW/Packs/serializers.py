from rest_framework import serializers
from .models import *
import zipfile
import json
from django.core.files import File



class PacksSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacksModel
        fields = ['name', 'logo', 'av_mana', 'description']
        
    
        
class Helper(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    logo = serializers.ImageField()
    
    def validate_name(self, value):
            if PacksModel.objects.filter(name=value):
                raise serializers.ValidationError("Name must be unique")
            return value


class UploadSerializer(serializers.Serializer):
    pack = serializers.FileField(allow_null=False, allow_empty_file=False)
    owner = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    
    def validate_pack(self, value):
        with zipfile.ZipFile(value.file, 'r') as pack:
            try:
                with pack.open('pack_info.json') as config:
                    cfg = json.load(config)
                    self.info = {}
                    self.info["name"] = cfg["PackItem_Title"]
                    self.info["description"] = cfg["PackItem_Description"]
                    try:
                        tmp = pack.open("pack_item_icon.png")
                        self.info["logo"] = File(tmp)
                    except:
                        raise serializers.ValidationError("Couldn't find a logo")
                    validator = Helper(data=self.info)
                    if not validator.is_valid():
                        raise serializers.ValidationError("Incorrect pack info")
                    self.cards = cfg["CustomInfoCards"]["$values"]
                    self.av_mana = 0
                    l = 0
                    for card in self.cards:
                        try:
                            s = f"Sprites/{card['ID']}.png"
                            print(s)
                            tmp = pack.open(s)
                            card["image"] = File(tmp)
                            card.pop("ID")
                            l+=1
                            self.av_mana+=card["ManaCost"]
                        except:
                            raise serializers.ValidationError("Couldn't find an image file")
                    self.av_mana = self.av_mana / l
                    return value
                        # raise serializers.ValidationError("Error while validating cards")
            except Exception as er:
                print(er)
                raise serializers.ValidationError("Cant read the pack file")
    
    def create(self, validated_data):
        obj = PacksModel.objects.create(**self.info,
                                        av_mana=self.av_mana, **validated_data)
        #obj.save()
        print(obj)
        for card in self.cards:
            card["pack"] = self.info["name"]
        self.cards_serializer = CardsSerializer(data=self.cards, many=True)
        if self.cards_serializer.is_valid():
            self.cards_serializer.create(self.cards_serializer.validated_data)
            self.cards_serializer.save()
            return obj
        else:
            print(self.cards_serializer.errors)
            raise serializers.ValidationError("error while validating cards")
        
    
class DownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacksModel
        fields = ['pack']
        

class CardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardsModel
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username", "rating", "pic")
        

class UpdatePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["pic"]