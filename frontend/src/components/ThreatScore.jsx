import React from 'react';
import {
  Box,
  Text,
  VStack,
  HStack,
  Badge,
  Progress,
} from '@chakra-ui/react';
import { getThreatLevel, getThreatColor } from '../types/threat';

const ThreatScore = ({ score, rationale }) => {
  const threatLevel = getThreatLevel(score);
  const color = getThreatColor(score);

  return (
    <Box
      p={6}
      borderWidth="2px"
      borderRadius="lg"
      borderColor={color}
      bg="gray.800"
      shadow="2xl"
    >
      <VStack spacing={4} align="stretch">
        <HStack justify="space-between" align="center">
          <Text fontSize="xl" fontWeight="bold" color="white">
            AI Threat Analysis
          </Text>
          <Badge
            colorScheme={threatLevel.color}
            fontSize="lg"
            px={4}
            py={1}
            borderRadius="full"
          >
            {threatLevel.label}
          </Badge>
        </HStack>

        <VStack spacing={2}>
          <Text fontSize="6xl" fontWeight="bold" color={color}>
            {score}
          </Text>
          <Text fontSize="sm" color="gray.600">
            Threat Score (0-100)
          </Text>
          <Progress
            value={score}
            size="lg"
            colorScheme={threatLevel.color}
            w="100%"
            borderRadius="full"
          />
        </VStack>

        <Box
          p={4}
          bg="gray.900"
          borderRadius="md"
          borderLeft="4px"
          borderColor={color}
        >
          <Text fontSize="sm" fontWeight="bold" mb={2} color="white">
            AI Rationale:
          </Text>
          <Text fontSize="sm" color="gray.300" lineHeight="tall">
            {rationale}
          </Text>
        </Box>
      </VStack>
    </Box>
  );
};

export default ThreatScore;
