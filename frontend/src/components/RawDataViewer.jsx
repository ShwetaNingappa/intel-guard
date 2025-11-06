import React from 'react';
import {
  Box,
  HStack,
  VStack,
  Button,
  IconButton,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  Text,
  useToast,
  Tooltip,
} from '@chakra-ui/react';
import { DownloadIcon, CopyIcon } from '@chakra-ui/icons';

const downloadBlob = (content, filename, type = 'application/json') => {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
};

const RawDataViewer = ({ rawData = {}, ip = 'ip' }) => {
  const toast = useToast();

  const sources = Object.keys(rawData || {});

  const handleDownloadAll = () => {
    const pretty = JSON.stringify(rawData, null, 2);
    const ts = new Date().toISOString().replace(/[:.]/g, '-');
    downloadBlob(pretty, `${ip}-raw_data-${ts}.json`);
  };

  const handleCopyAll = async () => {
    try {
      await navigator.clipboard.writeText(JSON.stringify(rawData, null, 2));
      toast({ title: 'Copied', description: 'Raw data copied to clipboard', status: 'success', duration: 2000 });
    } catch (e) {
      toast({ title: 'Copy failed', description: String(e), status: 'error', duration: 3000 });
    }
  };

  const handleDownloadOne = (key) => {
    const pretty = JSON.stringify(rawData[key] ?? {}, null, 2);
    const ts = new Date().toISOString().replace(/[:.]/g, '-');
    downloadBlob(pretty, `${ip}-${key}-raw-${ts}.json`);
  };

  const handleCopyOne = async (key) => {
    try {
      await navigator.clipboard.writeText(JSON.stringify(rawData[key] ?? {}, null, 2));
      toast({ title: 'Copied', description: `${key} JSON copied`, status: 'success', duration: 2000 });
    } catch (e) {
      toast({ title: 'Copy failed', description: String(e), status: 'error', duration: 3000 });
    }
  };

  return (
    <VStack align="stretch" spacing={4}>
      <HStack justify="space-between">
        <Text fontSize="lg" fontWeight="bold" color="white">Raw Data (All Sources)</Text>
        <HStack>
          <Tooltip label="Copy all JSON">
            <IconButton aria-label="copy-all" icon={<CopyIcon />} onClick={handleCopyAll} size="sm" />
          </Tooltip>
          <Button leftIcon={<DownloadIcon />} size="sm" onClick={handleDownloadAll} colorScheme="blue">
            Download JSON
          </Button>
        </HStack>
      </HStack>

      <Accordion allowMultiple>
        {sources.map((key) => (
          <AccordionItem key={key} borderColor="gray.700">
            <h2>
              <AccordionButton _hover={{ bg: 'gray.800' }}>
                <Box as="span" flex='1' textAlign='left' color="white" fontWeight="semibold">
                  {key}
                </Box>
                <HStack spacing={2} mr={2}>
                  <Tooltip label={`Copy ${key}`}>
                    <IconButton aria-label={`copy-${key}`} icon={<CopyIcon />} size="xs" onClick={(e) => { e.stopPropagation(); handleCopyOne(key); }} />
                  </Tooltip>
                  <Tooltip label={`Download ${key}`}>
                    <IconButton aria-label={`download-${key}`} icon={<DownloadIcon />} size="xs" onClick={(e) => { e.stopPropagation(); handleDownloadOne(key); }} />
                  </Tooltip>
                </HStack>
                <AccordionIcon />
              </AccordionButton>
            </h2>
            <AccordionPanel pb={4} bg="gray.900" color="green.300" borderTop="1px" borderColor="gray.700" fontSize="sm" fontFamily="monospace">
              <Box overflowX="auto">
                <pre>{JSON.stringify(rawData[key], null, 2)}</pre>
              </Box>
            </AccordionPanel>
          </AccordionItem>
        ))}
        {sources.length === 0 && (
          <Box p={4} bg="gray.800" color="gray.400" borderRadius="md" borderWidth="1px" borderColor="gray.700">
            No raw data available.
          </Box>
        )}
      </Accordion>
    </VStack>
  );
};

export default RawDataViewer;
