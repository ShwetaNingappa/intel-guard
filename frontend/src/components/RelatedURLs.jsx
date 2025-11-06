import React from 'react';
import { Box, Text, VStack, Link } from '@chakra-ui/react';

const RelatedURLs = ({ urls = [] }) => {
  const list = (urls || []).slice(0, 6);
  return (
    <Box p={4} borderWidth="1px" borderRadius="lg" bg="gray.800" borderColor="#2A2F3A" boxShadow="0 0 0 1px #2A2F3A, 0 0 16px rgba(0,255,255,0.08)">
      <VStack align="stretch" spacing={3}>
        <Text fontSize="lg" fontWeight="bold" color="white">Related Domains / URLs</Text>
        <VStack align="stretch" spacing={2}>
          {list.length === 0 && (
            <Text color="gray.500" fontSize="sm">No URLs found</Text>
          )}
          {list.map((u, idx) => (
            <Link key={idx} href={`https://www.virustotal.com/gui/search/${encodeURIComponent(u.url || '')}`} isExternal color="blue.400" _hover={{ color: 'blue.300' }}>
              {u.url || '—'}
            </Link>
          ))}
        </VStack>
      </VStack>
    </Box>
  );
};

export default RelatedURLs;
