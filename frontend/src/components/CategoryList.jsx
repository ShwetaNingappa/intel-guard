import React from 'react';
import { Box, Text, VStack, HStack } from '@chakra-ui/react';

const Dot = ({ active }) => (
  <Box w="10px" h="10px" borderRadius="full" bg={active ? 'red.400' : 'gray.600'} borderWidth="1px" borderColor={active ? 'red.500' : 'gray.700'} />
);

const CategoryList = ({ reputation={}, rationale='' }) => {
  const vtMal = reputation.virustotal_detections?.malicious ?? 0;
  const abuse = reputation.abuseipdb_score ?? 0;
  const otx = reputation.otx_pulse_count ?? 0;

  const categories = [
    { key: 'Botnet', active: vtMal > 0 || /botnet/i.test(rationale) },
    { key: 'Malware', active: vtMal > 0 || /malware/i.test(rationale) },
    { key: 'Phishing', active: abuse > 0 || /phish/i.test(rationale) },
    { key: 'Proxy', active: otx > 5 || /proxy/i.test(rationale) },
  ];

  return (
    <Box p={4} borderWidth="1px" borderRadius="lg" bg="gray.800" borderColor="#2A2F3A" boxShadow="0 0 0 1px #2A2F3A, 0 0 16px rgba(0,255,255,0.08)">
      <VStack align="stretch" spacing={3}>
        <Text fontSize="lg" fontWeight="bold" color="white">Categories</Text>
        {categories.map((c) => (
          <HStack key={c.key} spacing={3}>
            <Dot active={c.active} />
            <Text color={c.active ? 'red.300' : 'gray.400'}>{c.key}</Text>
          </HStack>
        ))}
      </VStack>
    </Box>
  );
};

export default CategoryList;
