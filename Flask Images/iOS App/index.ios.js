/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */

import React, { Component } from 'react';
import {
  AppRegistry,
  StyleSheet,
  Text,
  View,
  PixelRatio,
  TouchableOpacity,
  ActivityIndicator,
  Image,
  Dimensions,
} from 'react-native';

import ImagePicker from 'react-native-image-picker';

export default class AwesomeProject extends Component {

  state = {
    avatarSource: null,
    isLoading: false,
    message: ' ',
    translated: null,
    translatelanguage: 'es',
    helper: 'Tap on the square below to start',
    flag_es: 'https://github.com/stevenrskelton/flag-icon/raw/master/png/36/country-4x3/es.png'
  };

  selectPhotoTapped() {
    const options = {
      quality: 1.0,
      maxWidth: 500,
      maxHeight: 500,
      storageOptions: {
        skipBackup: true
      }
    };

    ImagePicker.showImagePicker(options, (response) => {
      console.log('Response = ', response);

      if (response.didCancel) {
        console.log('User cancelled photo picker');
      }
      else if (response.error) {
        console.log('ImagePicker Error: ', response.error);
      }
      else if (response.customButton) {
        console.log('User tapped custom button: ', response.customButton);
      }
      else {
        let source = { uri: response.uri };
        
        this.setState({
          isLoading: true,
          message: ' ',
          translated: null,
          helper: 'Running ...'
        });

        // You can also display the image using data:
        //let source = { uri: 'data:image/jpeg;base64,' + response.data }

        var photo = {
          uri: response.uri,
          type: 'image/jpeg',
          name: 'photo.jpg'
        };

        var body = new FormData()
        body.append('imagefile', photo)

        fetch('http://csabyy.uksouth.cloudapp.azure.com:5005/uploader_ios', {
          method: 'POST',
          body: body
        }).then((response) => response.json())
        .then((responseJson) => {
          var lk = this.state.translatelanguage
          this.setState({
            isLoading: false,
            message: responseJson.en,
            translated: responseJson[lk],
            helper: "Tap on the square to try another"
            });
        })

        this.setState({
          avatarSource: source
        });

      }
    });
  }

  render() {
    var spinner = this.state.isLoading ?
      ( <ActivityIndicator
          size='large'/> ) :
      ( <View/>);
    return (
      <View style={styles.container}>
        <Text style={styles.smalltext}>
          {this.state.helper}
        </Text>
        <TouchableOpacity onPress={this.selectPhotoTapped.bind(this)}>
          <View style={[styles.avatar, styles.avatarContainer, {marginBottom: 20}]}>
          { this.state.avatarSource === null ? <Text>Select a Photo</Text> :
            <Image style={styles.avatar} source={this.state.avatarSource} />
          }
          </View>
        </TouchableOpacity>

        <View style={{flex:1, marginTop:10}}>
        {spinner}
        </View>

        <View style={styles.languages}>
          <Text numberOfLines={1} style={styles.description}>
            {this.state.message}
          </Text>
        </View>

        <View style={styles.results}>
        <Text style={styles.smalltext}>
        Tap on flag to change language
        </Text>
          <View style={styles.languages}>
            <TouchableOpacity onPress={this.selectPhotoTapped.bind(this)}>
              <Image style={styles.flag} source={{uri: this.state.flag_es}} />
            </TouchableOpacity>
            <Text numberOfLines={1} style={styles.description}>
              {this.state.translated}
            </Text>
          </View>
        </View>

      </View>
    );
  }

}

var device_width = Dimensions.get('window').width;

const styles = StyleSheet.create({
  flag:{
    width: 36,
    height: 27,
    marginRight: 10
  },
  results:{
    alignSelf: 'flex-start'
  },
  languages:{
    flexDirection: 'row',
    marginBottom: 30
  },
  smalltext: {
    fontSize: 8,
    marginBottom: 10
  },
  description: {
    color: '#656565',
    fontSize: 18,
  },
  container: {
    padding: 30,
    justifyContent: 'center',
    alignItems: 'center',
  },
  avatarContainer: {
    borderColor: '#9B9B9B',
    borderWidth: 1 / PixelRatio.get(),
    justifyContent: 'center',
    alignItems: 'center'
  },
  avatar: {
    width: device_width,
    height: device_width
  }
});

AppRegistry.registerComponent('AwesomeProject', () => AwesomeProject);