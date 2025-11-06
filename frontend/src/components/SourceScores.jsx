import React from 'react';
import { Box, Text, VStack, HStack, Progress } from '@chakra-ui/react';

const Bar = ({ label, value }) => (
  <HStack justify="space-between" align="center">
    <Text color="gray.300" fontSize="sm">{label}</Text>
    <HStack w="60%" spacing={3} align="center">
      <Progress value={Math.max(0, Math.min(100, value || 0))} size="sm" colorScheme="red" w="100%" borderRadius="sm" />
      <Text color="gray.400" fontSize="xs" minW="28px" textAlign="right">{Math.round(value || 0)}</Text>
    </HStack>
  </HStack>
);

const SourceScores = ({ reputation={}, ownership={} }) => {
  const abuse = reputation.abuseipdb_score ?? 0;
  const vtMal = reputation.virustotal_detections?.malicious ?? 0;
  const vtScore = Math.min(100, vtMal * 5); // simple mapping
  const otx = Math.min(100, (reputation.otx_pulse_count ?? 0) * 5);
  const st = Math.min(100, (ownership.securitytrails_historical_count ?? 0));

  return (
    <Box p={4} borderWidth="1px" borderRadius="lg" bg="gray.800" borderColor="#2A2F3A" boxShadow="0 0 0 1px #2A2F3A, 0 0 16px rgba(0,255,255,0.08)">
      <VStack align="stretch" spacing={3}>
        <Text fontSize="lg" fontWeight="bold" color="white">Source Scores</Text>
        <Bar label="AbuseIPDB" value={abuse} />
        <Bar label="VirusTotal" value={vtScore} />
        <Bar label="OTX Pulses" value={otx} />
        <Bar label="SecurityTrails" value={st} />
      </VStack>
    </Box>
  );
};

export default SourceScores;
