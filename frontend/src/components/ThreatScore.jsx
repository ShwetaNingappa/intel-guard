import React from 'react';
import { Box, Text, VStack, HStack, Badge } from '@chakra-ui/react';
import { getThreatLevel, getThreatColor } from '../types/threat';

const ThreatScore = ({ score, rationale }) => {
  const threatLevel = getThreatLevel(score);
  const color = getThreatColor(score);
  const angle = Math.min(100, Math.max(0, Number(score) || 0)) * 3.6; // 0-360

  return (
    <Box p={6} borderWidth="1px" borderRadius="lg" bg="gray.800" borderColor="#2A2F3A" boxShadow="0 0 0 1px #2A2F3A, 0 0 16px rgba(0,255,255,0.08)">
      <HStack justify="space-between" mb={4}>
        <Text fontSize="lg" fontWeight="bold" color="white">Threat Score</Text>
        <Badge colorScheme={threatLevel.color} px={3} py={1} borderRadius="full">{threatLevel.label}</Badge>
      </HStack>

      <HStack spacing={8} align="center">
        {/* Donut gauge */}
        <Box position="relative" w="150px" h="150px">
          <Box
            position="absolute"
            inset={0}
            borderRadius="full"
            bg={`conic-gradient(${color} ${angle}deg, #2D3748 0deg)`}
            filter="drop-shadow(0 0 14px rgba(245, 101, 101, 0.35))"
          />
          <Box position="absolute" inset="14px" bg="gray.900" borderRadius="full" />
          <VStack position="absolute" inset={0} align="center" justify="center" spacing={0}>
            <Text fontSize="5xl" fontWeight="bold" color={color}>{score}</Text>
          </VStack>
        </Box>

        {/* Rationale */}
        <Box flex={1} p={4} bg="gray.900" borderRadius="md" borderWidth="1px" borderColor="#2A2F3A">
          <Text fontSize="sm" color="gray.300" lineHeight="tall">{rationale}</Text>
        </Box>
      </HStack>
    </Box>
  );
};

export default ThreatScore;
