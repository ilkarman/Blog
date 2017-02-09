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
  Image
} from 'react-native';

import ImagePicker from 'react-native-image-picker';

export default class AwesomeProject extends Component {
  state = {
    avatarSource: null,
    isLoading: false,
    message: null,
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

        var xhr = new XMLHttpRequest();

        xhr.onreadystatechange = (e) => {
          if (xhr.readyState !== 4) {
            return;
          }

          if (xhr.status === 200) {
            console.log('success', xhr.responseText);
            this.setState({
              isLoading: false,
              message: xhr.responseText,
              helper: "Tap on the square to try again"
            });
          } else {
            console.warn('error');
            this.setState({
              isLoading: false,
              message: "Error. Please try again ..."
            });
          }
        };

        xhr.open('POST', 'http://csabyy.uksouth.cloudapp.azure.com:5005/uploader_ios');
        xhr.send(body);

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
        <Text style={styles.description}>
          {this.state.message}
        </Text>
      </View>
    );
  }

}

const styles = StyleSheet.create({
  smalltext: {
    fontSize: 8,
    marginBottom: 10
  },
  description: {
    fontSize: 52,
    color: '#656565'
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
    borderRadius: 0,
    width: 244,
    height: 244
  }
});

AppRegistry.registerComponent('AwesomeProject', () => AwesomeProject);
