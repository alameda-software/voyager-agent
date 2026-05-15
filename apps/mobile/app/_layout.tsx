import { Stack } from "expo-router";
import { Platform, View, StyleSheet } from "react-native";

export default function RootLayout() {
  return (
    <View style={styles.root}>
      <Stack
        screenOptions={{
          animation: Platform.OS === 'web' ? 'none' : 'default',
          contentStyle: { backgroundColor: '#ffffff' },
          headerStyle: { backgroundColor: '#ffffff' },
        }}
      >
        <Stack.Screen name="index" options={{ headerShown: false }} />
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="+not-found" options={{ headerShown: false }} />
      </Stack>
    </View>
  );
}

const styles = StyleSheet.create({
  root: {
    flex: 1,
    width: '100%',
    maxWidth: '100%',
    overflow: 'hidden' as any,
    alignSelf: 'stretch',
  },
});
