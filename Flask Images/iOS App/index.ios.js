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
  Dimensions
} from 'react-native';

import ImagePicker from 'react-native-image-picker';

export default class AwesomeProject extends Component {
  state = {
    avatarSource: null,
    isLoading: false,
    message: null,
    translated: null,
    translatelanguage: 'es',
    helper: null
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
          message: null,
          translated: null,
          helper: null
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
            message: '(en) ' + responseJson.en,
            translated: '(' + lk + ') ' + responseJson[lk],
            helper: "Tap on the square to try again"
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
        {spinner}
        <Text numberOfLines={1} style={styles.description}>
          {this.state.message}
        </Text>
        <Text numberOfLines={1} style={styles.description}>
          {this.state.translated}
        </Text>
      </View>
    );
  }

}

var device_width = Dimensions.get('window').width;

const styles = StyleSheet.create({
  smalltext: {
    fontSize: 8,
    marginBottom: 10
  },
  description: {
    color: '#656565',
    fontSize: 24,
    marginBottom: 10
  },
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5FCFF'
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