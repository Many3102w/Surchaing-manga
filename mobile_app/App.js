import { StatusBar } from 'expo-status-bar';
import { StyleSheet, View, BackHandler, Platform, ActivityIndicator, Image, Text, Dimensions } from 'react-native';
import { WebView } from 'react-native-webview';
import React, { useRef, useEffect } from 'react';

const { width } = Dimensions.get('window');

import * as Notifications from 'expo-notifications';

// Configure notification behavior
Notifications.setNotificationHandler({
    handleNotification: async () => ({
        shouldShowAlert: true,
        shouldPlaySound: true,
        shouldSetBadge: false,
    }),
});

export default function App() {
    const webViewRef = useRef(null);
    const SERVER_URL = 'https://moda-gomez.onrender.com';

    // Request Permissions on load and Register Token
    useEffect(() => {
        const registerForPushNotificationsAsync = async () => {
            const { status: existingStatus } = await Notifications.getPermissionsAsync();
            let finalStatus = existingStatus;

            if (existingStatus !== 'granted') {
                const { status } = await Notifications.requestPermissionsAsync();
                finalStatus = status;
            }

            if (finalStatus !== 'granted') {
                console.warn('Failed to get push token for push notification!');
                return;
            }

            // Get the token
            const tokenData = await Notifications.getExpoPushTokenAsync({
                projectId: '01acf82b-dfe7-4a94-ba30-500db0961d9c',
            });
            const token = tokenData.data;
            console.log('Expo Push Token:', token);

            // Send to Backend
            // Note: We need the user to be logged in for this to work 100% correctly with our backend logic
            // But App.js runs on load. 
            // The WebView shares cookies? Yes, likely.
            // But fetching from RN side might not share the specific session cookie unless configured.
            // For now, let's try. If it fails (401), we might need to inject JS into WebView to post it.
            // OR simpler: Just inject it into the WebView so the WebView scripts post it.

            // BETTER STRATEGY: Inject the token into the WebView
            if (webViewRef.current) {
                webViewRef.current.injectJavaScript(`
                    window.EXPO_PUSH_TOKEN = '${token}';
                    if(window.registerToken) window.registerToken('${token}');
                `);
            }
            // Store it in ref to inject when WebView loads
            window.expoPushToken = token;
        };

        registerForPushNotificationsAsync();

        // Set up Android High Priority Channel
        if (Platform.OS === 'android') {
            Notifications.setNotificationChannelAsync('high_importance_channel', {
                name: 'High Importance Notifications',
                importance: Notifications.AndroidImportance.MAX,
                vibrationPattern: [0, 250, 250, 250],
                lightColor: '#FF231F7C',
            });
        }
    }, []);

    // Handle Android Back Button
    useEffect(() => {
        if (Platform.OS === 'android') {
            const onBackPress = () => {
                if (webViewRef.current) {
                    webViewRef.current.goBack();
                    return true;
                }
                return false;
            };

            BackHandler.addEventListener('hardwareBackPress', onBackPress);
            return () => BackHandler.removeEventListener('hardwareBackPress', onBackPress);
        }
    }, []);

    const handleMessage = async (event) => {
        try {
            const data = JSON.parse(event.nativeEvent.data);
            if (data.type === 'notification') {
                await Notifications.scheduleNotificationAsync({
                    content: {
                        title: data.title,
                        body: data.body,
                        data: data.data || {},
                    },
                    trigger: null, // immediate
                });
            }
        } catch (e) {
            console.warn("WebView Message Error", e);
        }
    };

    const LoadingScreen = () => (
        <View style={styles.loadingContainer}>
            <Image
                source={require('./assets/icon.png')}
                style={styles.loadingLogo}
                resizeMode="contain"
            />
            <ActivityIndicator size="large" color="#bfa37c" style={{ marginTop: 20 }} />
            <Text style={styles.loadingText}>Cargando DERSSG'M...</Text>
        </View>
    );

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
                renderLoading={LoadingScreen}
                scalesPageToFit={true}
                allowsBackForwardNavigationGestures={true}
                cacheEnabled={true}
                onMessage={handleMessage}
                onLoadEnd={() => {
                    // Inject token even if loaded after initial mount
                    if (window.expoPushToken && webViewRef.current) {
                        webViewRef.current.injectJavaScript(`
                            window.EXPO_PUSH_TOKEN = '${window.expoPushToken}';
                            if(window.registerToken) window.registerToken('${window.expoPushToken}');
                        `);
                    }
                }}
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
        marginTop: Platform.OS === 'android' ? 30 : 0,
    },
    loadingContainer: {
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: '#000',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 1,
    },
    loadingLogo: {
        width: width * 0.4,
        height: width * 0.4,
        borderRadius: 20,
    },
    loadingText: {
        color: '#fff',
        marginTop: 15,
        fontSize: 16,
        fontWeight: '600',
        letterSpacing: 1,
    }
});
