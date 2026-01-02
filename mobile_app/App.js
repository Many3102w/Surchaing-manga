import { StatusBar } from 'expo-status-bar';
import { StyleSheet, View, BackHandler, Platform } from 'react-native';
import { WebView } from 'react-native-webview';
import React, { useRef, useEffect } from 'react';

export default function App() {
    const webViewRef = useRef(null);
    const SERVER_URL = 'https://moda-gomez.onrender.com';

    // Handle Android Back Button to navigate content history instead of closing app
    useEffect(() => {
        if (Platform.OS === 'android') {
            const onBackPress = () => {
                if (webViewRef.current) {
                    webViewRef.current.goBack();
                    return true; // Prevent default behavior (exit)
                }
                return false;
            };

            BackHandler.addEventListener('hardwareBackPress', onBackPress);

            return () => BackHandler.removeEventListener('hardwareBackPress', onBackPress);
        }
    }, []);

    return (
        <View style={styles.container}>
            <StatusBar style="light" backgroundColor="#000000" />
            <WebView
                ref={webViewRef}
                source={{ uri: SERVER_URL }}
                style={styles.webview}
                javaScriptEnabled={true}
                domStorageEnabled={true}
                startInLoadingState={true}
                scalesPageToFit={true}
                allowsBackForwardNavigationGestures={true}
                // Cache optimization for 3D/assets
                cacheEnabled={true}
            />
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#000',
    },
    webview: {
        flex: 1,
        marginTop: 30, // Status bar offset
    },
});
