import type { ReactNode } from "react";
import { StyleSheet, useWindowDimensions, View, type ViewStyle } from "react-native";

import { colors, MOBILE_MAX_WIDTH } from "../theme";

interface MobileScreenProps {
  children: ReactNode;
  style?: ViewStyle;
  /** When false, children span full width of the column (default true = centered column). */
  padded?: boolean;
}

export function MobileScreen({ children, style, padded = true }: MobileScreenProps) {
  const { width } = useWindowDimensions();
  const columnWidth = Math.min(width, MOBILE_MAX_WIDTH);

  return (
    <View style={styles.outer}>
      <View style={[styles.column, { width: columnWidth, maxWidth: MOBILE_MAX_WIDTH }, padded && styles.padded, style]}>
        {children}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  outer: {
    flex: 1,
    backgroundColor: colors.background,
    alignItems: "center",
  },
  column: {
    flex: 1,
    width: "100%",
  },
  padded: {
    paddingHorizontal: 16,
  },
});
